from collections import OrderedDict
from dippy.core.caching.cacheable import Cacheable
from typing import Any, Callable, Generic, Optional, Type, TypeVar, Union
import logging


T = TypeVar("T", bound=Cacheable)
Factory = Union[Callable[[Cacheable], T], Type[T]]

log = logging.getLogger().getChild("Cache")


class Cache(Generic[T]):
    def __init__(self, max_size: int, factory: Factory):
        self._cache: OrderedDict[int, T] = OrderedDict()
        self._factory = factory
        self._max_size = max_size

    def add(self, payload: Cacheable, *args, **kwargs) -> bool:
        if not isinstance(payload, Cacheable):
            raise ValueError(
                f"The cache can only add items that derive from {Cacheable}, got {type(payload)}"
            )

        if payload.id not in self._cache:
            # It's a new item
            self._cache[payload.id] = self._factory(payload, *args, **kwargs)
            self._trim_cache()
            log.debug(f"Added {self._cache[payload.id]} to the cache {payload.created}")
        elif payload.created > self._cache[payload.id].created:
            # It's an updated item
            self._cache[payload.id].update(payload)
            self._cache.move_to_end(payload.id)
            log.debug(
                f"Updated {self._cache[payload.id]} in the cache {payload.created}"
            )
        else:
            # Not new and not newer
            log.debug(f"Ignored {self._cache[payload.id]}, newer in the cache")
            return False

        return True

    def remove(self, cache_id: int):
        item = self._cache.pop(cache_id, None)
        if item:
            log.debug(f"Removed {item} from the cache")

    def get(self, cache_id: int, default: Optional[Any] = None) -> T:
        if cache_id in self._cache:
            self._cache.move_to_end(cache_id)

        return self._cache.get(cache_id, default)

    def _trim_cache(self):
        while len(self._cache) > self._max_size:
            self._cache.popitem(last=False)
