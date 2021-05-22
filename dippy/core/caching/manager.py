from bevy import Context, Factory, Injectable
from dippy.core.caching.bases import BaseCacheManager
from dippy.core.caching.cache import Cache, MemberCache
from dippy.core.enums import Event
from dippy.core.events import BaseEventStream
from dippy.core.models.events import (
    EventChannelCreate,
    EventChannelDelete,
    EventChannelUpdate,
    EventGuildCreate,
    EventGuildDelete,
    EventGuildMemberAdd,
    EventGuildMemberRemove,
    EventGuildMemberUpdate,
    EventGuildMembersChunk,
    EventGuildUpdate,
    EventMessageCreate,
    EventMessageDelete,
    EventMessageDeleteBulk,
    EventMessageUpdate,
    GuildModel,
)
from dippy.core.interfaces.channel import Channel
from dippy.core.interfaces.guild import Guild
from dippy.core.interfaces.member import Member
from dippy.core.interfaces.message import Message
from dippy.core.interfaces.user import User
from typing import Union


class CacheManager(BaseCacheManager, Injectable):
    context: Context
    events: BaseEventStream

    def __init__(
        self,
        max_channels: int = 1000,
        max_guilds: int = 1_000,
        max_members: int = 10_000,
        max_messages: int = 1_000,
        max_users: int = 10_000,
    ):
        self._channels = Cache(max_channels, Factory(Channel, self.context))
        self._guilds = Cache(max_guilds, Factory(Guild, self.context))
        self._messages = Cache(max_messages, Factory(Message, self.context))
        self._members = MemberCache(max_members, Factory(Member, self.context))
        self._users = Cache(max_users, Factory(User, self.context))

        self.events.on(Event.CHANNEL_UPDATE, self.channel_update)
        self.events.on(Event.CHANNEL_CREATE, self.channel_update)
        self.events.on(Event.CHANNEL_DELETE, self.channel_remove)

        self.events.on(Event.GUILD_CREATE, self.guild_update)
        self.events.on(Event.GUILD_DELETE, self.guild_remove)
        self.events.on(Event.GUILD_UPDATE, self.guild_update)

        self.events.on(Event.GUILD_MEMBER_ADD, self.member_update)
        self.events.on(Event.GUILD_MEMBER_UPDATE, self.member_update)
        self.events.on(Event.GUILD_MEMBER_REMOVE, self.member_remove)
        self.events.on(Event.GUILD_MEMBERS_CHUNK, self.member_update_chunk)

        self.events.on(Event.MESSAGE_CREATE, self.message_update)
        self.events.on(Event.MESSAGE_UPDATE, self.message_update)
        self.events.on(Event.MESSAGE_DELETE, self.message_delete)
        self.events.on(Event.MESSAGE_DELETE_BULK, self.message_delete_bulk)

    @property
    def channels(self) -> Cache[Channel]:
        return self._channels

    @property
    def guilds(self) -> Cache[Guild]:
        return self._guilds

    @property
    def messages(self) -> Cache[Message]:
        return self._messages

    @property
    def members(self) -> MemberCache[tuple[Guild, Member]]:
        return self._members

    @property
    def users(self) -> Cache[User]:
        return self._users

    async def channel_update(
        self, event: Union[EventChannelCreate, EventChannelUpdate]
    ):
        self.channels.add(event)

    async def channel_remove(self, event: EventChannelDelete):
        self.channels.remove(event.id)

    async def channel_update_bulk(
        self, event: Union[EventGuildCreate, EventGuildUpdate, GuildModel]
    ):
        for channel in event.channels:
            self.channels.add(channel)

    async def guild_update(self, event: Union[EventGuildCreate, EventGuildUpdate]):
        self.guilds.add(event)
        await self.channel_update_bulk(event)
        await self.member_update_chunk(event)

    async def guild_remove(self, event: EventGuildDelete):
        self.guilds.remove(event.id)

    async def message_update(
        self, event: Union[EventMessageCreate, EventMessageUpdate]
    ):
        self.messages.add(event)

    async def message_delete(self, event: EventMessageDelete):
        self.messages.remove(event.id)

    async def message_delete_bulk(self, event: EventMessageDeleteBulk):
        for message_id in event.ids:
            self.messages.remove(message_id)

    async def member_update(
        self, event: Union[EventGuildMemberAdd, EventGuildMemberUpdate]
    ):
        if event.user:
            self.users.add(event.user)
        user = self.users.get(event.user.id)
        self.members.add(event, user)

    async def member_remove(self, event: EventGuildMemberRemove):
        self.members.remove(event.guild_id, event.user.id)

    async def member_update_chunk(
        self, event: Union[EventGuildMembersChunk, EventGuildCreate, EventGuildUpdate]
    ):
        for member in event.members:
            if member.user:
                self.users.add(member.user)

            member.guild_id = event.id or event.guild_id
            user = self.users.get(member.user.id)
            self.members.add(member, user)
