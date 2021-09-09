from attr import attrs, attrib
from dippy.core.datetime_helpers import datetime, from_string
from dippy.core.enums.channels import ChannelType, VideoQualityMode
from dippy.core.models.base_model import BaseModel
from dippy.core.models.permissions import PermissionOverwrite
from dippy.core.models.users import User
from dippy.core.snowflake import Snowflake
from typing import Optional


@attrs(auto_attribs=True)
class ThreadMetadata:
    archived: bool
    auto_archive_duration: int
    archive_timestamp: datetime = attrib(converter=from_string)
    locked: bool
    invitable: Optional[bool]


@attrs(auto_attribs=True)
class ThreadMember:
    id: Optional[Snowflake]  # Thread ID
    user_id: Optional[Snowflake]
    join_timestamp: datetime = attrib(converter=from_string)
    flags: int


class Channel(BaseModel):
    id: Snowflake
    type: ChannelType
    guild_id: Optional[Snowflake]
    position: Optional[int]
    permission_overwrites: Optional[list[PermissionOverwrite]]
    name: Optional[str]
    topic: Optional[str]
    nsfw: bool
    last_message_id: Optional[Snowflake]
    bitrate: Optional[int]
    user_limit: Optional[int]
    rate_limit_per_user: Optional[int]
    recipients: Optional[list[User]]
    icon: Optional[str]
    owner_id: Optional[Snowflake]
    application_id: Optional[Snowflake]
    parent_id: Optional[Snowflake]
    last_pin_timestamp: Optional[datetime]
    rtc_region: Optional[str]
    video_quality_mode: Optional[VideoQualityMode]
    message_count: Optional[int]
    member_count: Optional[int]
    thread_metadata: Optional[ThreadMetadata]
    member: Optional[ThreadMember]
    default_auto_archive_duration: Optional[int]
    permissions: Optional[str]
