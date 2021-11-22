from __future__ import annotations
from dippy.core.api.request import RequestModel, QueryArgField, URLArgField
from dippy.core.api.models.guilds import Guild, Member
from dippy.core.snowflake import Snowflake


class GetGuildMember(RequestModel):
    endpoint = "/guilds/{guild_id}/members/{user_id}"
    method = "GET"
    model = Member

    guild_id: Snowflake = URLArgField(index=True)
    user_id: Snowflake = URLArgField(index=True)


class GetGuild(RequestModel):
    endpoint = "/guilds/{id}"
    method = "GET"
    model = Guild

    id: Snowflake = URLArgField(index=True, key_name="guild_id")

    with_counts: bool = QueryArgField()
