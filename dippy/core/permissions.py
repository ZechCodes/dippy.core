from dataclasses import dataclass
from dippy.core.enums import ChannelType
from dippy.core.interfaces.member import Member


class InsufficientPermissions(Exception):
    pass


@dataclass
class Permission:
    name: str
    description: str
    value: int
    channel_type: list[ChannelType]
    requires_mfa: bool

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self} mfa={self.requires_mfa} channels={self.channel_type} {self.description!r}>"


class Permissions:
    @classmethod
    def has_require_permission(cls, member: Member, *required_permissions) -> bool:
        # Todo: Write this function
        return True

    CREATE_INSTANT_INVITE = Permission(
        "CREATE_INSTANT_INVITE",
        "Allows creation of instant invites",
        0x000000001,
        [ChannelType.TEXT, ChannelType.VOICE, ChannelType.STAGE],
        False,
    )
    KICK_MEMBERS = Permission(
        "KICK_MEMBERS", "Allows kicking members", 0x000000002, [], True
    )
    BAN_MEMBERS = Permission(
        "BAN_MEMBERS", "Allows banning members", 0x000000004, [], True
    )
    ADMINISTRATOR = Permission(
        "ADMINISTRATOR",
        "Allows all permissions and bypasses channel permission overwrites",
        0x000000008,
        [],
        True,
    )
    MANAGE_CHANNELS = Permission(
        "MANAGE_CHANNELS",
        "Allows management and editing of channels",
        0x000000010,
        [ChannelType.TEXT, ChannelType.VOICE, ChannelType.STAGE],
        True,
    )
    MANAGE_GUILD = Permission(
        "MANAGE_GUILD",
        "Allows management and editing of the guild",
        0x000000020,
        [],
        True,
    )
    ADD_REACTIONS = Permission(
        "ADD_REACTIONS",
        "Allows for the addition of reactions to messages",
        0x000000040,
        [ChannelType.TEXT],
        False,
    )
    VIEW_AUDIT_LOG = Permission(
        "VIEW_AUDIT_LOG", "Allows for viewing of audit logs", 0x000000080, [], False
    )
    PRIORITY_SPEAKER = Permission(
        "PRIORITY_SPEAKER",
        "Allows for using priority speaker in a voice channel",
        0x000000100,
        [ChannelType.VOICE],
        False,
    )
    STREAM = Permission(
        "STREAM", "Allows the user to go live", 0x000000200, [ChannelType.VOICE], False
    )
    VIEW_CHANNEL = Permission(
        "VIEW_CHANNEL",
        "Allows guild members to view a channel, which includes reading messages in text channels",
        0x000000400,
        [ChannelType.TEXT, ChannelType.VOICE, ChannelType.STAGE],
        False,
    )
    SEND_MESSAGES = Permission(
        "SEND_MESSAGES",
        "Allows for sending messages in a channel",
        0x000000800,
        [ChannelType.TEXT],
        False,
    )
    SEND_TTS_MESSAGES = Permission(
        "SEND_TTS_MESSAGES",
        "Allows for sending of /tts messages",
        0x000001000,
        [ChannelType.TEXT],
        False,
    )
    MANAGE_MESSAGES = Permission(
        "MANAGE_MESSAGES",
        "Allows for deletion of other users messages",
        0x000002000,
        [ChannelType.TEXT],
        True,
    )
    EMBED_LINKS = Permission(
        "EMBED_LINKS",
        "Links sent by users with this permission will be auto-embedded",
        0x000004000,
        [ChannelType.TEXT],
        False,
    )
    ATTACH_FILES = Permission(
        "ATTACH_FILES",
        "Allows for uploading images and files",
        0x000008000,
        [ChannelType.TEXT],
        False,
    )
    READ_MESSAGE_HISTORY = Permission(
        "READ_MESSAGE_HISTORY",
        "Allows for reading of message history",
        0x000010000,
        [ChannelType.TEXT],
        False,
    )
    MENTION_EVERYONE = Permission(
        "MENTION_EVERYONE",
        "Allows for using the @everyone tag to notify all users in a channel, and the @here tag to notify all online "
        "users in a channel",
        0x000020000,
        [ChannelType.TEXT],
        False,
    )
    USE_EXTERNAL_EMOJIS = Permission(
        "USE_EXTERNAL_EMOJIS",
        "Allows the usage of custom emojis from other servers",
        0x000040000,
        [ChannelType.TEXT],
        False,
    )
    VIEW_GUILD_INSIGHTS = Permission(
        "VIEW_GUILD_INSIGHTS",
        "Allows for viewing guild insights",
        0x000080000,
        [],
        False,
    )
    CONNECT = Permission(
        "CONNECT",
        "Allows for joining of a voice channel",
        0x000100000,
        [ChannelType.VOICE, ChannelType.STAGE],
        False,
    )
    SPEAK = Permission(
        "SPEAK",
        "Allows for speaking in a voice channel",
        0x000200000,
        [ChannelType.VOICE],
        False,
    )
    MUTE_MEMBERS = Permission(
        "MUTE_MEMBERS",
        "Allows for muting members in a voice channel",
        0x000400000,
        [ChannelType.VOICE, ChannelType.STAGE],
        False,
    )
    DEAFEN_MEMBERS = Permission(
        "DEAFEN_MEMBERS",
        "Allows for deafening of members in a voice channel",
        0x000800000,
        [ChannelType.VOICE, ChannelType.STAGE],
        False,
    )
    MOVE_MEMBERS = Permission(
        "MOVE_MEMBERS",
        "Allows for moving of members between voice channels",
        0x001000000,
        [ChannelType.VOICE, ChannelType.STAGE],
        False,
    )
    USE_VAD = Permission(
        "USE_VAD",
        "Allows for using voice-activity-detection in a voice channel",
        0x002000000,
        [ChannelType.VOICE, ChannelType.STAGE],
        False,
    )
    CHANGE_NICKNAME = Permission(
        "CHANGE_NICKNAME",
        "Allows for modification of own nickname",
        0x004000000,
        [],
        False,
    )
    MANAGE_NICKNAMES = Permission(
        "MANAGE_NICKNAMES",
        "Allows for modification of other users nicknames",
        0x008000000,
        [],
        False,
    )
    MANAGE_ROLES = Permission(
        "MANAGE_ROLES",
        "Allows management and editing of roles",
        0x010000000,
        [ChannelType.TEXT, ChannelType.VOICE, ChannelType.STAGE],
        True,
    )
    MANAGE_WEBHOOKS = Permission(
        "MANAGE_WEBHOOKS",
        "Allows management and editing of webhooks",
        0x020000000,
        [ChannelType.TEXT],
        True,
    )
    MANAGE_EMOJIS = Permission(
        "MANAGE_EMOJIS",
        "Allows management and editing of emojis",
        0x040000000,
        [],
        True,
    )
    USE_SLASH_COMMANDS = Permission(
        "USE_SLASH_COMMANDS",
        "Allows members to use slash commands in text channels",
        0x080000000,
        [ChannelType.TEXT],
        False,
    )
    REQUEST_TO_SPEAK = Permission(
        "REQUEST_TO_SPEAK",
        "Allows for requesting to speak in stage channels. (This permission is under active development and may be "
        "changed or removed.)",
        0x100000000,
        [ChannelType.STAGE],
        False,
    )
