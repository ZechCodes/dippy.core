from collections import defaultdict
from dippy.core.snowflake import Snowflake
from typing import Any, Protocol, Optional, TypeVar, Union


DiscordObject = dict[str, Any]
Key = Union[Snowflake, int, str, Any]
ModelType = TypeVar("ModelType")


class CacheProtocol(Protocol[ModelType]):
    def __init__(self, cache_manager):
        ...

    def get(self, key: Key) -> Optional[DiscordObject]:
        ...

    def update(self, key: Key, data: DiscordObject):
        ...


class Cache:
    def __init__(self):
        self._cache: dict[Key, DiscordObject] = defaultdict(dict)

    def get(self, key: Key) -> Optional[DiscordObject]:
        return self._cache.get(key)

    def update(self, key: Key, data: DiscordObject):
        self._cache[key].update(data)
