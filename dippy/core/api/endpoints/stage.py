from __future__ import annotations
from typing import Optional
from dippy.core.api.request import RequestModel, URLArgField, JSONArgField
from dippy.core.snowflake import Snowflake


class CreateStageInstance(RequestModel):
    endpoint = "/stage-instances"
    method = "POST"

    channel_id: Snowflake = JSONArgField()
    topic: str = JSONArgField()
    privacy_level: Optional[int] = JSONArgField()


class GetStageInstance(RequestModel):
    endpoint = "/stage-instances/{channel_id}"
    method = "GET"

    channel_id: Snowflake = URLArgField()


class ModifyStageInstance(RequestModel):
    endpoint = "/stage-instances/{channel_id}"
    method = "GET"

    channel_id: Snowflake = URLArgField()

    topic: Optional[str] = JSONArgField()
    privacy_level: Optional[int] = JSONArgField()


class DeleteStageInstance(RequestModel):
    endpoint = "/stage-instances/{channel_id}"
    method = "DELETE"

    channel_id = URLArgField()
