from datetime import datetime
from dippy.core.caching.cacheable import Cacheable
from dippy.core.models.activity import ActivityModel
from dippy.core.models.application import ApplicationModel, ApplicationCommandModel
from dippy.core.models.channel import ChannelModel
from dippy.core.models.client_status import ClientStatusModel
from dippy.core.models.emoji import EmojiModel
from dippy.core.models.guild import GuildModel
from dippy.core.models.interaction import InteractionModel
from dippy.core.models.member import MemberModel
from dippy.core.models.message import MessageModel
from dippy.core.models.presence import PresenceModel
from dippy.core.models.role import RoleModel
from dippy.core.models.user import UserModel
from dippy.core.models.voice_state import VoiceStateModel
from dippy.core.timestamp import Timestamp
from pydantic import BaseModel, Field, validator
from dippy.core.snowflake import Snowflake
from typing import Optional


class EventModel(BaseModel):
    pass


class CacheableUser(BaseModel, Cacheable):
    created: Timestamp = Field(default_factory=Timestamp)

    @property
    def id(self) -> Snowflake:
        return self.user.id


def make_event_object(event, base):
    return type(event, (base,), {})


class EventChannelCreate(ChannelModel):
    pass


class EventChannelUpdate(ChannelModel):
    pass


class EventChannelDelete(ChannelModel):
    pass


class EventReady(EventModel):
    v: int
    user: UserModel
    session_id: str
    relationships: list
    private_channels: list


class EventChannelPinsUpdate(EventModel):
    channel_id: Snowflake
    guild_id: Optional[Snowflake]
    last_pin_timestamp: Optional[datetime]


class _PartialGuildModel(EventModel, Cacheable):
    def __new__(cls, *args, **kwargs):
        if not kwargs.get("unavailable", len(kwargs) <= 2):
            return GuildModel(**kwargs)
        return super().__new__(cls)

    id: Snowflake
    unavailable: bool = Field(default=True)


class EventGuildCreate(_PartialGuildModel):
    pass


class EventGuildUpdate(_PartialGuildModel):
    pass


class EventGuildDelete(_PartialGuildModel):
    pass


class EventGuildMemberAdd(MemberModel):
    pass


class _EventGuildBanUpdate(EventModel):
    guild_id: Snowflake
    user: UserModel


class EventGuildBanAdd(_EventGuildBanUpdate):
    pass


class EventGuildBanRemove(_EventGuildBanUpdate):
    pass


class EventGuildEmojisUpdate(EventModel):
    guild_id: Snowflake
    emojis: list[EmojiModel]


class EventGuildIntegrationsUpdate(EventModel):
    guild_id: Snowflake


class EventGuildMemberRemove(CacheableUser):
    guild_id: Snowflake
    user: UserModel


class EventGuildMemberUpdate(CacheableUser):
    guild_id: Snowflake
    roles: list[Snowflake]
    user: UserModel
    nick: Optional[str]
    joined_at: datetime
    premium_since: Optional[datetime]
    deaf: Optional[bool]
    mute: Optional[bool]
    pending: Optional[bool]


class EventGuildMembersChunk(EventModel):
    guild_id: Snowflake
    members: list[MemberModel]
    chunk_index: int
    chunk_count: int
    not_found: Optional[bool]
    presences: Optional[list[PresenceModel]]
    nonce: Optional[str]


class _EventGuildRoleUpdate(EventModel):
    guild_id: Snowflake
    role: RoleModel


class EventGuildRoleCreate(_EventGuildRoleUpdate):
    pass


class EventGuildRoleUpdate(_EventGuildRoleUpdate):
    pass


class EventGuildRoleDelete(EventModel):
    guild_id: Snowflake
    role_id: Snowflake


class _EventIntegrationUpdate(EventModel):
    guild_id: Snowflake


EventIntegrationCreate = make_event_object(
    "EventIntegrationCreate", _EventIntegrationUpdate
)
EventIntegrationUpdate = make_event_object(
    "EventIntegrationUpdate", _EventIntegrationUpdate
)


class EventIntegrationDelete(EventModel):
    id: Snowflake
    guild_id: Snowflake
    application_id: Optional[Snowflake]


class EventInviteCreate(EventModel):
    channel_id: Snowflake
    code: str
    created_at: datetime
    guild_id: Optional[Snowflake]
    inviter: UserModel
    max_age: int
    max_uses: int
    target_type: Optional[Snowflake]
    target_user: Optional[UserModel]
    target_application: Optional[ApplicationModel]
    temporary: bool
    uses: int


class EventInviteDelete(EventModel):
    channel_id: Snowflake
    guild_id: Optional[Snowflake]


class EventMessageCreate(MessageModel):
    pass


class EventMessageUpdate(MessageModel):
    pass


class EventMessageDelete(EventModel):
    id: Snowflake
    channel_id: Snowflake
    guild_id: Optional[Snowflake]


class EventMessageDeleteBulk(EventModel):
    ids: list[Snowflake]
    channel_id: Snowflake
    guild_id: Optional[Snowflake]


class EventMessageReactionAdd(EventModel):
    user_id: Snowflake
    channel_id: Snowflake
    message_id: Snowflake
    guild_id: Optional[Snowflake]
    member: Optional[MemberModel]
    emoji: EmojiModel


EventMessageReactionRemove = make_event_object(
    "EventMessageReactionRemove", EventMessageReactionAdd
)


class EventMessageReactionRemoveAll(EventModel):
    channel_id: Snowflake
    message_id: Snowflake
    guild_id: Optional[Snowflake]


class EventMessageReactionRemoveEmoji(EventMessageReactionRemoveAll):
    emoji: EmojiModel


class EventPresenceUpdate(EventModel):
    user_id: Snowflake = Field(alias="user")
    guild_id: Snowflake
    status: str
    activities: list[ActivityModel]
    client_status: ClientStatusModel

    @validator("user_id", pre=True)
    def get_user_id(cls, value):
        return Snowflake(value.get("id"))


class EventTypingStart(EventModel):
    channel_id: Optional[Snowflake]
    guild_id: Optional[Snowflake]
    user_id: Snowflake
    timestamp: datetime
    member: Optional[MemberModel]


class EventUserUpdate(UserModel):
    pass


class EventVoiceStateUpdate(VoiceStateModel):
    pass


class EventVoiceServerUpdate(EventModel):
    token: str
    guild_id: Snowflake
    endpoint: Optional[str]


class EventWebhooksUpdate(EventModel):
    guild_id: Snowflake
    channel_id: Snowflake


EventApplicationCommandCreate = make_event_object(
    "EventApplicationCommandCreate", ApplicationCommandModel
)
EventApplicationCommandUpdate = make_event_object(
    "EventApplicationCommandUpdate", ApplicationCommandModel
)
EventApplicationCommandDelete = make_event_object(
    "EventApplicationCommandDelete", ApplicationCommandModel
)


class EventInteractionCreate(InteractionModel):
    pass
