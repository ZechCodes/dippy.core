from dippy.core.enums.enums import IntEnum, StrEnum


class MessageType(IntEnum):
    DEFAULT = 0
    RECIPIENT_ADD = 1
    RECIPIENT_REMOVE = 2
    CALL = 3
    CHANNEL_NAME_CHANGE = 4
    CHANNEL_ICON_CHANGE = 5
    CHANNEL_PINNED_MESSAGE = 6
    GUILD_MEMBER_JOIN = 7
    USER_PREMIUM_GUILD_SUBSCRIPTION = 8
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_1 = 9
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_2 = 10
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_3 = 11
    CHANNEL_FOLLOW_ADD = 12
    GUILD_DISCOVERY_DISQUALIFIED = 14
    GUILD_DISCOVERY_REQUALIFIED = 15
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    THREAD_CREATED = 18
    REPLY = 19
    APPLICATION_COMMAND = 20
    THREAD_STARTER_MESSAGE = 21
    GUILD_INVITE_REMINDER = 22


class MessageActivityType(IntEnum):
    JOIN = 1
    SPECTATE = 2
    LISTEN = 3
    JOIN_REQUEST = 4


class EmbedType(StrEnum):
    RICH = "rich"  # generic embed rendered from embed attributes
    IMAGE = "image"  # image embed
    VIDEO = "video"  # video embed
    GIF = "gifv"  # animated gif image embed rendered as a video embed
    ARTICLE = "article"  # article embed
    LINK = "link"  # link embed


# FIXME: Don't believe this class should remain in this file. Maybe create a new one for mentions?
class AllowedMentionsType(StrEnum):
    ROLE_MENTIONS = "roles"  # Controls role mentions
    USER_MENTIONS = "users"  # Controls user mentions
    EVERYONE_MENTIONS = "everyone"  # Controls @everyone and @here mentions


class ComponentType(IntEnum):
    ACTION_ROW = 1  # A container for other components
    BUTTON = 2  # A button object
    SELECT_MENU = 3  # A select menu for picking from choices


class ButtonStyle(IntEnum):
    PRIMARY = 1  # blurple
    SECONDARY = 2  # grey
    SUCCESS = 3  # green
    DANGER = 4  # red
    LINK = 5  # grey, navigates to a URL
