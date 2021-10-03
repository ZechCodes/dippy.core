from __future__ import annotations
from bevy.inject import Injectable
from bevy.factory import Factory
from collections import defaultdict
from dippy.core.cache.cache import Cache, DiscordObject, Key
from typing import Optional, Type
import dippy.core.model as m


class CacheManager(Injectable):
    create_cache = Factory(Cache)

    def __init__(self):
        self._caches: dict[str, Cache] = defaultdict(self.create_cache)

    def get(self, model: Type[m.ModelType], *key: Key) -> Optional[m.ModelType]:
        data = self._caches[model.__dippy_cache_type__].get(key)
        return self.__bevy_context__.build(model, data) if data else None

    def update(self, model: Type[m.ModelType], data: DiscordObject, *key: Key):
        key = key if key else self.get_key(model, data)
        self._caches[model.__dippy_cache_type__].update(key, data)

    def get_key(self, model: m.ModelType, data: DiscordObject) -> Key:
        return tuple(data[key] for key in model.__dippy_index_fields__)
