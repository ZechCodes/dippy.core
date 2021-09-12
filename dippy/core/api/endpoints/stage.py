from __future__ import annotations
from typing import Optional
from dippy.core.api.request import request_model, json_arg, url_arg
from dippy.core.snowflake import Snowflake


@request_model
class CreateStageInstance:
    endpoint = "/stage-instances"
    method = "POST"

    channel_id: Snowflake = json_arg()
    topic: str = json_arg()
    privacy_level: Optional[int] = json_arg()


@request_model
class GetStageInstance:
    endpoint = "/stage-instances/{channel_id}"
    method = "GET"

    channel_id: Snowflake = url_arg()


@request_model
class ModifyStageInstance:
    endpoint = "/stage-instances/{channel_id}"
    method = "GET"

    channel_id: Snowflake = url_arg()

    topic: Optional[str] = json_arg()
    privacy_level: Optional[int] = json_arg()


@request_model
class DeleteStageInstance:
    endpoint = "/stage-instances/{channel_id}"
    method = "DELETE"

    channel_id = url_arg()
