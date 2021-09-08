from dippy.core.enums.enums import IntEnum

# TODO: Maybe include https://discord.com/developers/docs/resources/channel#channel-object-video-quality-modes
# TODO: to this file..


class ChannelTypes(IntEnum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_NEWS = 5
    GUILD_STORE = 6
    GUILD_NEWS_THREAD = 10
    GUILD_PUBLIC_THREAD = 11
    GUILD_PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13
