from __future__ import annotations
from attr import attrs
from dippy.core.datetime_helpers import datetime
from dippy.core.enums.guilds import (
    ExplicitContentFilterLevel,
    GuildFeature,
    NSFWLevel,
    NotificationLevel,
    PremiumTier,
    SystemChannelFlags,
    TwoFactorAuthentication,
    VerificationLevel,
)
from dippy.core.models.base_model import BaseModel
from dippy.core.models.channels import Channel, Stage
from dippy.core.models.emoji import Emoji
from dippy.core.models.permissions import Role
from dippy.core.models.presences import Presence
from dippy.core.models.stickers import Sticker
from dippy.core.models.users import User
from dippy.core.snowflake import Snowflake
from typing import Optional


@attrs(auto_attribs=True)
class VoiceState:
    guild_id: Optional[Snowflake]
    channel_id: Optional[Snowflake]
    user_id: Snowflake
    member: Member
    session_id: str
    deaf: bool
    mute: bool
    self_deaf: bool
    self_mute: bool
    self_stream: bool
    self_video: bool
    suppress: bool
    request_to_speak_timestamp: Optional[datetime]


class Member(BaseModel):
    user: Optional[User]
    nick: Optional[str]
    roles: list[Snowflake]
    joined_at: datetime
    premium_since: Optional[datetime]
    deaf: bool
    mute: bool
    pending: Optional[bool]
    permissions: Optional[str]


@attrs(auto_attribs=True)
class WelcomeScreen:
    description: Optional[str]
    welcome_channels: list[WelcomeScreenChannel]


class Guild(BaseModel):
    id: Snowflake
    name: str
    icon: Optional[str]
    icon_hash: Optional[str]
    splash: Optional[str]
    discovery_splash: Optional[str]
    owner: Optional[bool]
    owner_id: Snowflake
    permissions: Optional[str]
    region: Optional[str]
    afk_channel_id: Optional[Snowflake]
    afk_timeout: int
    widget_enabled: Optional[bool]
    widget_channel_id: Optional[Snowflake]
    verification_level: VerificationLevel
    default_message_notifications: NotificationLevel
    explicit_content_filter: ExplicitContentFilterLevel
    roles: list[Role]
    emojis: list[Emoji]
    features: list[GuildFeature]
    mfa_level: TwoFactorAuthentication
    application_id: Optional[Snowflake]
    system_channel_id: Optional[Snowflake]
    system_channel_flags: SystemChannelFlags
    rules_channel_id: Optional[Snowflake]
    joined_at: Optional[datetime]
    large: Optional[bool]
    unavailable: Optional[bool]
    member_count: Optional[int]
    voice_states: Optional[list[VoiceState]]
    members: Optional[list[Member]]
    channels: Optional[list[Channel]]
    threads: Optional[list[Channel]]
    presences: Optional[list[Presence]]
    max_presences: Optional[int]
    max_members: Optional[int]
    vanity_url_code: Optional[str]
    description: Optional[str]
    banner: Optional[str]
    premium_tier: PremiumTier
    premium_subscription_count: Optional[int]
    preferred_locale: str
    public_updates_channel_id: Optional[Snowflake]
    max_video_channel_users: Optional[int]
    approximate_member_count: Optional[int]
    approximate_presence_count: Optional[int]
    welcome_screen: WelcomeScreen
    nsfw_level: Optional[NSFWLevel]
    stage_instances: Optional[list[Stage]]
    stickers: Optional[list[Sticker]]


@attrs(auto_attribs=True)
class WelcomeScreenChannel:
    channel_id: Snowflake
    description: str
    emoji_id: Optional[Snowflake]
    emoji_name: Optional[str]
