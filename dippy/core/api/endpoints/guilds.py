from __future__ import annotations
from dippy.core.api.request import request_model, url_arg
from dippy.core.snowflake import Snowflake


@request_model
class GetGuildMember:
    endpoint = "/guilds/{guild_id}/members/{user_id}"
    method = "GET"

    guild_id: Snowflake = url_arg()
    user_id: Snowflake = url_arg()
