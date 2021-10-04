from __future__ import annotations
from dippy.core.api.request import request_model, query_arg, url_arg
from dippy.core.api.models.guilds import Guild, Member
from dippy.core.snowflake import Snowflake


@request_model
class GetGuildMember:
    endpoint = "/guilds/{guild_id}/members/{user_id}"
    method = "GET"
    model = Member

    guild_id: Snowflake = url_arg()
    user_id: Snowflake = url_arg()

    def get_index(self, request: GetGuildMember) -> tuple[Snowflake, Snowflake]:
        return self.guild_id, Snowflake(request["user"]["id"])


@request_model
class GetGuild:
    endpoint = "/guilds/{guild_id}"
    method = "GET"
    model = Guild

    guild_id: Snowflake = url_arg()

    with_counts: bool = query_arg()
