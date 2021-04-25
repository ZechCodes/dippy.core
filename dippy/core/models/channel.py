from datetime import datetime
from dippy.core.enums import ChannelType
from dippy.core.models.model import DippyCoreModel, DippyCoreCacheableModel
from dippy.core.models.overwrite import OverwriteModel
from dippy.core.models.user import UserModel
from dippy.core.snowflake import Snowflake
from typing import Optional


class ChannelMentionModel(DippyCoreModel):
    id: Snowflake
    guild_id: Snowflake
    type: ChannelType
    name: str


class ChannelModel(DippyCoreCacheableModel):
    id: Snowflake
    type: ChannelType

    application_id: Optional[Snowflake]
    bitrate: Optional[int]
    created_at: Optional[datetime]
    guild_id: Optional[Snowflake]
    icon: Optional[str]
    last_message_id: Optional[Snowflake]
    last_pin_timestamp: Optional[datetime]
    name: Optional[str]
    nsfw: Optional[bool]
    owner_id: Optional[Snowflake]
    parent_id: Optional[Snowflake]
    permission_overwrites: list[OverwriteModel]
    position: Optional[int]
    rate_limit_per_user: Optional[int]
    recipients: Optional[list[UserModel]]
    rtc_region: Optional[str]
    topic: Optional[str]
    user_limit: Optional[int]
    video_quality_mode: Optional[int]
