from __future__ import annotations

from abc import ABC, abstractmethod
from bevy import Injectable
from dippy.core.gateway.payload import Payload
from gully import Gully, Observer
from typing import Any, Awaitable, Callable, Coroutine, Optional, Union
import dippy.core.models.events as events


EventHandler = Union[
    Callable[[events.EventModel], None], Coroutine[None, events.EventModel, None]
]
Filter = Callable[[Any], bool]
FilterFactory = Callable[[Any], Filter]
Mapper = Callable[[Any], Any]


class BaseEventDispatch(ABC):
    @property
    @abstractmethod
    def next(self) -> Awaitable:
        ...

    @abstractmethod
    def on(self, *args, **kwargs) -> Observer:
        ...


class EventRegistry(BaseEventDispatch):
    def __init__(
        self,
        filter_factory: FilterFactory,
        stream: Gully,
        *,
        mapper: Optional[Mapper] = None,
    ):
        self._stream = stream
        self._filter_factory = filter_factory
        self._filters: dict[Any, Gully] = {}
        self._mapper = mapper

    @property
    def next(self) -> Awaitable:
        return self._stream.next

    def on(self, *args, **kwargs) -> Observer:
        *args, callback = args
        key = (tuple(args), tuple(kwargs.items()))
        if key not in self._filters:
            filtered = self._stream.filter(self._filter_factory(*args, **kwargs))
            if self._mapper:
                filtered = filtered.map(self._mapper)
            self._filters[key] = filtered
        return self._filters[key].watch(callback)


class BaseEventStream(BaseEventDispatch, ABC, Injectable):
    @property
    @abstractmethod
    def raw(self) -> EventRegistry:
        ...

    @abstractmethod
    def push(self, payload: Payload):
        ...


class EventDispatch(BaseEventStream, Injectable):
    def __init__(self):
        self._stream = Gully()
        self._raw_event_registry = EventRegistry(self._raw_filter_factory, self._stream)
        self._event_registry = EventRegistry(
            self._event_filter_factory,
            self._stream.filter(self._only_discord_events),
            mapper=self._create_event,
        )

    @property
    def next(self) -> Awaitable:
        return self._event_registry.next

    @property
    def raw(self) -> EventRegistry:
        return self._raw_event_registry

    def on(self, event: str, callback: EventHandler) -> Observer:
        return self._event_registry.on(event, callback)

    def push(self, payload: Payload):
        self._stream.push(payload)

    def _create_event(self, payload: Payload) -> events.EventModel:
        name = self._get_event_name(payload.event)
        model = getattr(events, name, None)
        if not model:
            print("COULDN'T FIND", name)
            return events.make_event_object(name, payload.event)

        try:
            return model(**payload.data)
        except:
            import pprint

            print(payload.event)
            pprint.pp(payload.data)
            raise

    def _event_filter_factory(self, *event_names: str) -> Filter:
        return (
            lambda payload: event_names[0].casefold() in {"any", "all", "*"}
            or payload.event in event_names
        )

    def _get_event_name(self, event: str) -> str:
        cleaned = "".join(section.capitalize() for section in event.split("_"))
        return f"Event{cleaned}"

    def _only_discord_events(self, payload: Payload) -> bool:
        return bool(payload.event)

    def _raw_filter_factory(self, *, op_code: int = None, event: str = None) -> Filter:
        return lambda payload: (payload.op_code == op_code or op_code is None) and (
            payload.event == event or event is None
        )
