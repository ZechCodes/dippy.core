from __future__ import annotations
from dippy.core.api.request import request_model, url_arg
from dippy.core.snowflake import Snowflake


@request_model
class GetChannelRequest:
    endpoint = "/channels/{channel_id}"
    method = "GET"

    channel_id: Snowflake = url_arg()
