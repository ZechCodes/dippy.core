from dippy.core.caching.cache import Cache
from dippy.core.enums import Event as E
from dippy.core.gateway.connection import GatewayConnection
from dippy.core.gateway.event_mapper import Event
from dippy.core.interfaces.channel import Channel
from dippy.core.interfaces.guild import Guild
from dippy.core.interfaces.member import Member
from dippy.core.interfaces.message import Message
from dippy.core.interfaces.user import User


class CacheManager:
    def __init__(
        self,
        gateway: GatewayConnection,
        max_channels: int = 1000,
        max_guilds: int = 1_000,
        max_members: int = 10_000,
        max_messages: int = 1_000,
        max_users: int = 10_000,
    ):
        self.channels = Cache(max_channels, Channel)
        self.guilds = Cache(max_guilds, Guild)
        self.messages = Cache(max_messages, Message)
        self.members = Cache(max_members, Member)
        self.users = Cache(max_users, User)

        gateway.on(E.CHANNEL_CREATE, self.channel_update)
        gateway.on(E.CHANNEL_UPDATE, self.channel_update)
        gateway.on(E.CHANNEL_DELETE, self.channel_remove)

        gateway.on(E.GUILD_CREATE, self.guild_update)
        gateway.on(E.GUILD_UPDATE, self.guild_update)
        gateway.on(E.GUILD_DELETE, self.guild_remove)

        gateway.on(E.GUILD_MEMBER_ADD, self.member_update)
        gateway.on(E.GUILD_MEMBER_UPDATE, self.member_update)
        gateway.on(E.GUILD_MEMBER_REMOVE, self.member_remove)
        gateway.on(E.GUILD_MEMBERS_CHUNK, self.member_update_chunk)

        gateway.on(E.MESSAGE_CREATE, self.message_update)
        gateway.on(E.MESSAGE_UPDATE, self.message_update)
        gateway.on(E.MESSAGE_DELETE, self.message_delete)
        gateway.on(E.MESSAGE_DELETE_BULK, self.message_delete_bulk)

    async def channel_update(self, event: Event):
        self.channels.add(event.payload)

    async def channel_remove(self, event: Event):
        self.channels.remove(event.payload.id)

    async def channel_update_bulk(self, event: Event):
        for channel in event.payload.channels:
            self.channels.add(channel)

    async def guild_update(self, event: Event):
        self.guilds.add(event.payload)
        await self.channel_update_bulk(event)
        await self.member_update_chunk(event)

    async def guild_remove(self, event: Event):
        self.guilds.remove(event.payload.id)

    async def message_update(self, event: Event):
        self.messages.add(event.payload)

    async def message_delete(self, event: Event):
        self.messages.remove(event.payload.id)

    async def message_delete_bulk(self, event: Event):
        for message_id in event.payload.ids:
            self.messages.remove(message_id)

    async def member_update(self, event: Event):
        if event.payload.user:
            self.users.add(event.payload.user)
        user = self.users.get(event.payload.user.id)
        self.members.add(event.payload, user)

    async def member_remove(self, event: Event):
        self.members.remove(event.payload.id)

    async def member_update_chunk(self, event: Event):
        for member in event.payload.members:
            if member.user:
                self.users.add(member.user)
            user = self.users.get(member.user.id)
            self.members.add(member, user)
