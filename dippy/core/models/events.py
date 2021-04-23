from datetime import datetime
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
from pydantic import BaseModel, Field, validator
from dippy.core.snowflake import Snowflake
from typing import Optional


class _EventModel(BaseModel):
    pass


def _make_event_object(event, base):
    return type(event, (base,), {})


EventChannelCreate = _make_event_object("EventChannelCreate", ChannelModel)
EventChannelUpdate = _make_event_object("EventChannelUpdate", ChannelModel)
EventChannelDelete = _make_event_object("EventChannelDelete", ChannelModel)

EventGuildCreate = _make_event_object("EventGuildCreate", GuildModel)
EventGuildUpdate = _make_event_object("EventGuildUpdate", GuildModel)
EventGuildMemberAdd = _make_event_object("EventGuildMemberAdd", MemberModel)


class EventReady(_EventModel):
    v: int
    user: UserModel
    session_id: str
    relationships: list
    private_channels: list


class EventChannelPinsUpdate(_EventModel):
    channel_id: Snowflake
    guild_id: Optional[Snowflake]
    last_pin_timestamp: Optional[datetime]


class _PartialGuildModel(_EventModel):
    id: Snowflake
    unavailable: bool


def _event_guild_delete(**kwargs):
    if kwargs.get("unavailable", False):
        return _PartialGuildModel(**kwargs)
    return GuildModel(**kwargs)


EventGuildDelete = _event_guild_delete


class _EventGuildBanUpdate(_EventModel):
    guild_id: Snowflake
    user: UserModel


EventGuildBanAdd = _make_event_object("EventGuildBanAdd", _EventGuildBanUpdate)
EventGuildBanRemove = _make_event_object("EventGuildBanRemove", _EventGuildBanUpdate)


class EventGuildEmojisUpdate(_EventModel):
    guild_id: Snowflake
    emojis: list[EmojiModel]


class EventGuildIntegrationsUpdate(_EventModel):
    guild_id: Snowflake


class EventGuildMemberRemove(_EventModel):
    guild_id: Snowflake
    user: UserModel


class EventGuildMemberUpdate(_EventModel):
    guild_id: Snowflake
    roles: list[Snowflake]
    user: UserModel
    nick: Optional[str]
    joined_at: datetime
    premium_since: Optional[datetime]
    deaf: Optional[bool]
    mute: Optional[bool]
    pending: Optional[bool]


class EventGuildMembersChunk(_EventModel):
    guild_id: Snowflake
    members: list[MemberModel]
    chunk_index: int
    chunk_count: int
    not_found: Optional[bool]
    presences: Optional[list[PresenceModel]]
    nonce: Optional[str]


class _EventGuildRoleUpdate(_EventModel):
    guild_id: Snowflake
    role: RoleModel


EventGuildRoleCreate = _make_event_object("EventGuildRoleCreate", _EventGuildRoleUpdate)
EventGuildRoleUpdate = _make_event_object("EventGuildRoleUpdate", _EventGuildRoleUpdate)


class EventGuildRoleDelete(_EventModel):
    guild_id: Snowflake
    role_id: Snowflake


class _EventIntegrationUpdate(_EventModel):
    guild_id: Snowflake


EventIntegrationCreate = _make_event_object(
    "EventIntegrationCreate", _EventIntegrationUpdate
)
EventIntegrationUpdate = _make_event_object(
    "EventIntegrationUpdate", _EventIntegrationUpdate
)


class EventIntegrationDelete(_EventModel):
    id: Snowflake
    guild_id: Snowflake
    application_id: Optional[Snowflake]


class EventInviteCreate(_EventModel):
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


class EventInviteDelete(_EventModel):
    channel_id: Snowflake
    guild_id: Optional[Snowflake]


EventMessageCreate = _make_event_object("EventMessageCreate", MessageModel)
EventMessageUpdate = _make_event_object("EventMessageUpdate", MessageModel)


class EventMessageDelete(_EventModel):
    id: Snowflake
    channel_id: Snowflake
    guild_id: Optional[Snowflake]


class EventMessageDeleteBulk(_EventModel):
    ids: list[Snowflake]
    channel_id: Snowflake
    guild_id: Optional[Snowflake]


class EventMessageReactionAdd(_EventModel):
    user_id: Snowflake
    channel_id: Snowflake
    message_id: Snowflake
    guild_id: Optional[Snowflake]
    member: Optional[MemberModel]
    emoji: EmojiModel


EventMessageReactionRemove = _make_event_object(
    "EventMessageReactionRemove", EventMessageReactionAdd
)


class EventMessageReactionRemoveAll(_EventModel):
    channel_id: Snowflake
    message_id: Snowflake
    guild_id: Optional[Snowflake]


class EventMessageReactionRemoveEmoji(EventMessageReactionRemoveAll):
    emoji: EmojiModel


class EventPresenceUpdate(_EventModel):
    user_id: Snowflake = Field(alias="user")
    guild_id: Snowflake
    status: str
    activities: list[ActivityModel]
    client_status: ClientStatusModel

    @validator("user_id", pre=True)
    def get_user_id(cls, value):
        return Snowflake(value.get("id"))


class EventTypingStart(_EventModel):
    channel_id: Optional[Snowflake]
    guild_id: Optional[Snowflake]
    user_id: Snowflake
    timestamp: datetime
    member: Optional[MemberModel]


EventUserUpdate = _make_event_object("EventUserUpdate", UserModel)
EventVoiceStateUpdate = _make_event_object("EventVoiceStateUpdate", VoiceStateModel)


class EventVoiceServerUpdate(_EventModel):
    token: str
    guild_id: Snowflake
    endpoint: Optional[str]


class EventWebhookUpdate(_EventModel):
    guild_id: Snowflake
    channel_id: Snowflake


EventApplicationCommandCreate = _make_event_object(
    "EventApplicationCommandCreate", ApplicationCommandModel
)
EventApplicationCommandUpdate = _make_event_object(
    "EventApplicationCommandUpdate", ApplicationCommandModel
)
EventApplicationCommandDelete = _make_event_object(
    "EventApplicationCommandDelete", ApplicationCommandModel
)
EventInteractionCreate = _make_event_object("EventInteractionCreate", InteractionModel)
