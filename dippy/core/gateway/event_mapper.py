from dippy.core.models import events
from dippy.core.gateway.payload import Payload
from typing import TypeVar, Union


T = TypeVar("T")


class Event:
    def __init__(self, event: str, model: T):
        self._event = event
        self._data = model

    @property
    def event(self) -> str:
        return self._event

    @property
    def payload(self) -> T:
        return self._data


def event_mapper(event: Payload) -> Union[Event, Payload]:
    if not event.event:
        return event

    name = _get_event_name(event.event)
    model = getattr(events, name, None)
    if not model:
        print("COULDN'T FIND", name)
        return event

    try:
        return Event(event.event, model(**event.data))
    except:
        import pprint

        print(event.event)
        pprint.pp(event.data)
        raise


def _get_event_name(event: str) -> str:
    cleaned = "".join(section.capitalize() for section in event.split("_"))
    return f"Event{cleaned}"
