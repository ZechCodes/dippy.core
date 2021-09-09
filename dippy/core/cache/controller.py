from collections import defaultdict
from dippy.core.snowflake import Snowflake
from typing import Any, Generic, Protocol, Optional, TypeVar, Union


DiscordObject = dict[str, Any]
ID = Union[Snowflake, int]
ModelType = TypeVar("ModelType")


def id_maker(object_id: ID):
    if isinstance(object_id, Snowflake):
        return object_id
    return Snowflake(object_id)


class CacheController(Protocol[ModelType]):
    def __init__(self, cache_manager):
        ...

    def get(self, object_id) -> Optional[DiscordObject]:
        ...

    def update(self, object_id, data):
        ...


class BasicController:
    def __init__(self, cache_manager):
        self._manager = cache_manager
        self._cache: dict[Snowflake, DiscordObject] = defaultdict(dict)

    def get(self, object_id: ID) -> Optional[DiscordObject]:
        return self._cache.get(id_maker(object_id))

    def update(self, object_id: ID, data: DiscordObject):
        self._cache[id_maker(object_id)].update(data)


class MemberController:
    def __init__(self, cache_manager):
        self._cache_manager = cache_manager
        self._cache: dict[Snowflake, dict[Snowflake, DiscordObject]] = defaultdict(
            lambda: defaultdict(dict)
        )

    def get(self, guild_id: ID, member_id: ID) -> Optional[DiscordObject]:
        return self._cache[id_maker(guild_id)].get(id_maker(member_id))

    def update(self, guild_id: ID, member_id: ID, data: DiscordObject):
        self._cache[id_maker(guild_id)][id_maker(member_id)].update(data)
