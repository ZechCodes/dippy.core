from dippy.core.enums.enums import IntFlag, IntEnum, StrEnum


class VerificationLevel(IntEnum):
    NONE = 0  # unrestricted
    LOW = 1  # must have verified email on account
    MEDIUM = 2  # must be registered on Discord for longer than 5 minutes
    HIGH = 3  # must be a member of the server for longer than 10 minutes
    VERY_HIGH = 4  # must have a verified phone number


class NotificationLevel(IntEnum):
    ALL_MESSAGES = 0  # members will receive notifications for all messages by default
    ONLY_MENTIONS = 1  # members will receive notifications only for messages that @mention them by default


class ExplicitContentFilterLevel(IntEnum):
    DISABLED = 0  # media content will not be scanned
    MEMBERS_WITHOUT_ROLES = 1  # media content sent by members w/o roles will be scanned
    ALL_MEMBERS = 2  # media content sent by all members will be scanned


class TwoFactorAuthentication(IntEnum):
    NONE = 0  # guild has no MFA/2FA requirement for moderation actions
    ELEVATED = 1  # guild has a 2FA requirement for moderation actions


class SystemChannelFlags(IntFlag):
    SUPPRESS_JOIN_NOTIFICATIONS = 1 << 0  # Suppress member join notifications
    SUPPRESS_PREMIUM_SUBSCRIPTIONS = 1 << 1  # Suppress server boost notifications
    SUPPRESS_GUILD_REMINDER_NOTIFICATIONS = 1 << 2  # Suppress server setup tips


class PremiumTier(IntEnum):
    NONE = 0  # guild has not unlocked any Server Boost perks
    TIER_1 = 1  # guild has unlocked Server Boost level 1 perks
    TIER_2 = 2  # guild has unlocked Server Boost level 2 perks
    TIER_3 = 3  # guild has unlocked Server Boost level 3 perks


class NSFWLevel(IntEnum):
    DEFAULT = 0
    EXPLICIT = 1
    SAFE = 2
    AGE_RESTRICTED = 3


class GuildFeature(StrEnum):
    ANIMATED_ICON = "ANIMATED_ICON"  # guild has access to set an animated guild icon
    BANNER = "BANNER"  # guild has access to set a guild banner image
    COMMERCE = "COMMERCE"  # guild has access to use commerce features (i.e. create store channels)
    COMMUNITY = "COMMUNITY"  # guild can enable welcome screen, Membership Screening, stage channels and discovery, and receives community updates
    DISCOVERABLE = "DISCOVERABLE"  # guild is able to be discovered in the directory
    FEATURABLE = "FEATURABLE"  # guild is able to be featured in the directory
    INVITE_SPLASH = (
        "INVITE_SPLASH"  # guild has access to set an invite splash background
    )
    MEMBER_VERIFICATION_GATE_ENABLED = (
        "MEMBER_VERIFICATION_GATE_ENABLED"  # guild has enabled Membership Screening
    )
    NEWS = "NEWS"  # guild has access to create news channels
    PARTNERED = "PARTNERED"  # guild is partnered
    PREVIEW_ENABLED = "PREVIEW_ENABLED"  # guild can be previewed before joining via Membership Screening or the directory
    VANITY_URL = "VANITY_URL"  # guild has access to set a vanity URL
    VERIFIED = "VERIFIED"  # guild is verified
    VIP_REGIONS = "VIP_REGIONS"  # guild has access to set 384kbps bitrate in voice (previously VIP voice servers)
    WELCOME_SCREEN_ENABLED = (
        "WELCOME_SCREEN_ENABLED"  # guild has enabled the welcome screen
    )
    TICKETED_EVENTS_ENABLED = (
        "TICKETED_EVENTS_ENABLED"  # guild has enabled ticketed events
    )
    MONETIZATION_ENABLED = "MONETIZATION_ENABLED"  # guild has enabled monetization
    MORE_STICKERS = "MORE_STICKERS"  # guild has increased custom sticker slots
    THREE_DAY_THREAD_ARCHIVE = "THREE_DAY_THREAD_ARCHIVE"  # guild has access to the three day archive time for threads
    SEVEN_DAY_THREAD_ARCHIVE = "SEVEN_DAY_THREAD_ARCHIVE"  # guild has access to the seven day archive time for threads
    PRIVATE_THREADS = "PRIVATE_THREADS"  # guild has access to create private threads
