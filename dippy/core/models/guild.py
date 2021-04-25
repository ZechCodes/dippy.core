from datetime import datetime
from dippy.core.enums import (
    DefaultMessageNotificationLevel,
    ExplicitContentFilterLevel,
    GuildFeature,
    MFALevel,
    PremiumTier,
    VerificationLevel,
)
from dippy.core.models.channel import ChannelModel
from dippy.core.models.emoji import EmojiModel
from dippy.core.models.member import MemberModel
from dippy.core.models.model import DippyCoreModel, DippyCoreCacheableModel
from dippy.core.models.presence import PresenceModel
from dippy.core.models.role import RoleModel
from dippy.core.models.voice_state import VoiceStateModel
from dippy.core.snowflake import Snowflake
from typing import Optional, Union


class WelcomeScreenChannelModel(DippyCoreModel):
    channel_id: Snowflake
    description: str
    emoji_id: Optional[Snowflake]
    emoji_name: Optional[str]


class WelcomeScreenModel(DippyCoreModel):
    description: Optional[str]
    welcome_channels: Optional[list[WelcomeScreenChannelModel]]


class GuildModel(DippyCoreCacheableModel):
    afk_timeout: int
    default_message_notifications: DefaultMessageNotificationLevel
    emojis: list[EmojiModel]
    explicit_content_filter: ExplicitContentFilterLevel
    features: list[GuildFeature]
    id: Snowflake
    name: str
    nsfw: bool
    owner_id: Snowflake
    preferred_locale: str
    premium_tier: PremiumTier
    region: str
    roles: list[RoleModel]
    system_channel_flags: int
    verification_level: VerificationLevel

    afk_channel_id: Optional[Snowflake]
    application_id: Optional[Snowflake]
    approximate_member_count: Optional[int]
    approximate_presence_count: Optional[int]
    banner: Optional[str]
    channels: Optional[list[ChannelModel]]
    description: Optional[str]
    discovery_splash: Optional[str]
    icon: Optional[str]
    icon_hash: Optional[str]
    joined_at: Optional[datetime]
    large: Optional[bool]
    max_members: Optional[int]
    max_presences: Optional[int]
    max_video_channel_users: Optional[int]
    member_count: Optional[int]
    members: Optional[list[MemberModel]]
    mfa: Optional[MFALevel]
    mfa_level: Optional[MFALevel]
    owner: Optional[bool]
    permissions: Optional[str]
    premium_subscription_count: Optional[int]
    presences: Optional[list[PresenceModel]]
    public_updates_channel_id: Optional[Snowflake]
    rules_channel_id: Optional[Snowflake]
    splash: Optional[Union[int, str]]
    system_channel_id: Optional[Snowflake]
    unavailable: Optional[bool]
    vanity_url_code: Optional[str]
    voice_states: Optional[list[VoiceStateModel]]
    welcome_screen: Optional[WelcomeScreenModel]
    widget_channel_id: Optional[Snowflake]
    widget_enabled: Optional[bool]
