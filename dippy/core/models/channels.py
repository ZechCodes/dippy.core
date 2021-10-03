from __future__ import annotations
from dippy.core.datetime_helpers import datetime
from dippy.core.enums.channels import ChannelType, PrivacyLevel, VideoQualityMode
from dippy.core.model import Model, Field
from dippy.core.models.applications import Application
from dippy.core.models.guilds import Guild
from dippy.core.models.messages import Message
from dippy.core.models.permissions import PermissionOverwrite
from dippy.core.models.users import User
from dippy.core.snowflake import Snowflake
from typing import Optional


class ThreadMetadata(Model):
    archived: bool
    auto_archive_duration: int
    archive_timestamp: datetime
    locked: bool
    invitable: Optional[bool]


class ThreadMember(Model):
    thread: Optional[Channel] = Field(key_name="id", index=True)  # Thread ID
    user: Optional[User] = Field(key_name="user_id")
    join_timestamp: datetime
    flags: int


class Channel(Model, cache_type="channel"):
    id: Snowflake = Field(index=True)
    type: ChannelType
    guild: Optional[Guild] = Field(key_name="guild_id")
    position: Optional[int]
    permission_overwrites: Optional[list[PermissionOverwrite]]
    name: Optional[str]
    topic: Optional[str]
    nsfw: bool
    last_message: Optional[Message] = Field(key_name="last_message_id")
    bitrate: Optional[int]
    user_limit: Optional[int]
    rate_limit_per_user: Optional[int]
    recipients: Optional[list[User]]
    icon: Optional[str]
    owner: Optional[User] = Field(key_name="owner_id")
    application: Optional[Application] = Field(key_name="application_id")
    parent: Optional[Channel] = Field(key_name="parent_id")
    last_pin_timestamp: Optional[datetime]
    rtc_region: Optional[str]
    video_quality_mode: Optional[VideoQualityMode]
    message_count: Optional[int]
    member_count: Optional[int]
    thread_metadata: Optional[ThreadMetadata]
    member: Optional[ThreadMember]
    default_auto_archive_duration: Optional[int]
    permissions: Optional[str]


class Stage(Model, cach_type="channel"):
    id: Snowflake = Field(index=True)
    guild: Guild = Field(key_name="guild_id")
    channel: Channel = Field(key_name="channel_id")
    topic: str
    privacy_level: PrivacyLevel
    discoverable_disabled: bool
