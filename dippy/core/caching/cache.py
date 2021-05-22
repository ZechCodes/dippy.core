from collections import OrderedDict
from dippy.core.caching.cacheable import Cacheable
from typing import Any, Callable, Generic, Hashable, Optional, Type, TypeVar, Union
import logging


T = TypeVar("T", bound=Cacheable)
Factory = Union[Callable[[Cacheable], T], Type[T]]

log = logging.getLogger().getChild("Cache")


class Cache(Generic[T]):
    def __init__(self, max_size: int, factory: Factory):
        self._cache: OrderedDict[Hashable, T] = OrderedDict()
        self._factory = factory
        self._max_size = max_size

    def add(self, payload: Cacheable, *args, **kwargs) -> Optional[T]:
        if not isinstance(payload, Cacheable):
            raise ValueError(
                f"The cache can only add items that derive from {Cacheable}, got {type(payload)}"
            )

        key = self._determine_key(payload, *args, **kwargs)

        if key not in self._cache:
            # It's a new item
            self._cache[key] = self._factory(payload, *args, **kwargs)
            self._trim_cache()
            log.debug(f"Added {self._cache[key]} to the cache {payload.created}")
        elif payload.created > self._cache[key].created:
            # It's an updated item
            self._cache[key].update(payload)
            self._cache.move_to_end(key)
            log.debug(f"Updated {self._cache[key]} in the cache {payload.created}")
        else:
            # Not new and not newer
            log.debug(f"Ignored {self._cache[key]}, newer in the cache")
            return

        return self._cache[key]

    def remove(self, cache_id: int):
        item = self._cache.pop(cache_id, None)
        if item:
            log.debug(f"Removed {item} from the cache")

    def get(self, cache_id: int, default: Optional[Any] = None) -> T:
        if cache_id in self._cache:
            self._cache.move_to_end(cache_id)

        return self._cache.get(cache_id, default)

    def _determine_key(self, payload: Cacheable, *args, **kwargs) -> Hashable:
        return payload.id

    def _trim_cache(self):
        while len(self._cache) > self._max_size:
            self._cache.popitem(last=False)


class MemberCache(Cache, Generic[T]):
    def _determine_key(self, payload: Cacheable, *args, **kwargs) -> Hashable:
        return payload.guild_id, payload.id

    def remove(self, guild_id: int, user_id: Optional[int] = None):
        if not user_id:
            self._remove_all_members(guild_id)
            return

        item = self._cache.pop((guild_id, user_id), None)
        if item:
            log.debug(f"Removed {item} from the cache")

    def get(self, guild_id: int, user_id: int, default: Optional[Any] = None) -> T:
        key = (guild_id, user_id)
        if key in self._cache:
            self._cache.move_to_end(key)

        return self._cache.get(key, default)

    def _remove_all_members(self, guild_id: int):
        for key_guild_id, user_id in self._cache:
            if guild_id == key_guild_id:
                self.remove(guild_id, user_id)
