from datetime import datetime
from dippy.core.models.channel import ChannelModel
from dippy.core.models.emoji import EmojiModel
from dippy.core.models.member import MemberModel
from dippy.core.models.model import DippyCoreModel
from dippy.core.models.presence import PresenceModel
from dippy.core.models.role import RoleModel
from dippy.core.snowflake import Snowflake
from typing import Optional, Union


class GuildModel(DippyCoreModel):
    afk_channel_id: Optional[Snowflake]
    application_id: Optional[Snowflake]
    banner: Optional[str]
    channels: list[ChannelModel]
    default_message_notifications: int
    description: Optional[str]
    discovery_splash: Optional[str]
    emojis: list[EmojiModel]
    explicit_content_filter: int
    features: list
    icon: Optional[str]
    id: Snowflake
    joined_at: datetime
    large: bool
    lazy: bool
    max_members: int
    max_video_channel_users: int
    member_count: int
    members: list[MemberModel]
    mfa_level: int
    name: str
    nsfw: bool
    owner_id: Snowflake
    preferred_locale: str
    premium_subscription_count: int
    premium_tier: int
    presences: list[PresenceModel]
    public_updates_channel_id: Optional[Snowflake]
    region: str
    roles: list[RoleModel]
    rules_channel_id: Optional[Snowflake]
    splash: Optional[Union[int, str]]
    stage_instances: list
    system_channel_flags: int
    system_channel_id: Snowflake
    threads: list
    unavailable: bool
    vanity_url_code: Optional[int]
    verification_level: int
    voice_states: list
