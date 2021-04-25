from __future__ import annotations
from dippy.core.caching.cacheable import Cacheable
from dippy.core.models.guild import *
from dippy.core.timestamp import Timestamp
from gully import Gully


class Guild(Cacheable):
    def __init__(self, model: GuildModel):
        self._model = model
        self._change_event_stream = Gully()

    def update(self, model: GuildModel):
        print(self._model.afk_channel_id)
        self._model = self._model.copy(update=model.dict(exclude_unset=True))
        print(self._model.afk_channel_id)

    def freeze(self) -> Guild:
        return Guild(self._model)

    @property
    def created(self) -> Timestamp:
        return self._model.created

    @property
    def afk_timeout(self) -> int:
        return self._model.afk_timeout

    @property
    def default_message_notifications(self) -> DefaultMessageNotificationLevel:
        return self._model.default_message_notifications

    @property
    def emojis(self) -> list[EmojiModel]:
        return self._model.emojis

    @property
    def explicit_content_filter(self) -> ExplicitContentFilterLevel:
        return self._model.explicit_content_filter

    @property
    def features(self) -> list[GuildFeature]:
        return self._model.features

    @property
    def id(self) -> Snowflake:
        return self._model.id

    @property
    def name(self) -> str:
        return self._model.name

    @property
    def nsfw(self) -> bool:
        return self._model.nsfw

    @property
    def owner_id(self) -> Snowflake:
        return self._model.owner_id

    @property
    def preferred_locale(self) -> str:
        return self._model.preferred_locale

    @property
    def premium_tier(self) -> PremiumTier:
        return self._model.premium_tier

    @property
    def region(self) -> str:
        return self._model.region

    @property
    def roles(self) -> list[RoleModel]:
        return self._model.roles

    @property
    def system_channel_flags(self) -> int:
        return self._model.system_channel_flags

    @property
    def verification_level(self) -> VerificationLevel:
        return self._model.verification_level

    @property
    def afk_channel_id(self) -> Optional[Snowflake]:
        return self._model.afk_channel_id

    @property
    def application_id(self) -> Optional[Snowflake]:
        return self._model.application_id

    @property
    def approximate_member_count(self) -> Optional[int]:
        return self._model.approximate_member_count

    @property
    def approximate_presence_count(self) -> Optional[int]:
        return self._model.approximate_presence_count

    @property
    def banner(self) -> Optional[str]:
        return self._model.banner

    @property
    def channels(self) -> Optional[list[ChannelModel]]:
        return self._model.channels

    @property
    def description(self) -> Optional[str]:
        return self._model.description

    @property
    def discovery_splash(self) -> Optional[str]:
        return self._model.discovery_splash

    @property
    def icon(self) -> Optional[str]:
        return self._model.icon

    @property
    def icon_hash(self) -> Optional[str]:
        return self._model.icon_hash

    @property
    def joined_at(self) -> Optional[datetime]:
        return self._model.joined_at

    @property
    def large(self) -> Optional[bool]:
        return self._model.large

    @property
    def max_members(self) -> Optional[int]:
        return self._model.max_members

    @property
    def max_presences(self) -> Optional[int]:
        return self._model.max_presences

    @property
    def max_video_channel_users(self) -> Optional[int]:
        return self._model.max_video_channel_users

    @property
    def member_count(self) -> Optional[int]:
        return self._model.member_count

    @property
    def members(self) -> Optional[list[MemberModel]]:
        return self._model.members

    @property
    def mfa(self) -> Optional[MFALevel]:
        return self._model.mfa

    @property
    def mfa_level(self) -> Optional[MFALevel]:
        return self._model.mfa_level

    @property
    def owner(self) -> Optional[bool]:
        return self._model.owner

    @property
    def permissions(self) -> Optional[str]:
        return self._model.permissions

    @property
    def premium_subscription_count(self) -> Optional[int]:
        return self._model.premium_subscription_count

    @property
    def presences(self) -> Optional[list[PresenceModel]]:
        return self._model.presences

    @property
    def public_updates_channel_id(self) -> Optional[Snowflake]:
        return self._model.public_updates_channel_id

    @property
    def rules_channel_id(self) -> Optional[Snowflake]:
        return self._model.rules_channel_id

    @property
    def splash(self) -> Optional[Union[int, str]]:
        return self._model.splash

    @property
    def system_channel_id(self) -> Optional[Snowflake]:
        return self._model.system_channel_id

    @property
    def unavailable(self) -> Optional[bool]:
        return self._model.unavailable

    @property
    def vanity_url_code(self) -> Optional[str]:
        return self._model.vanity_url_code

    @property
    def voice_states(self) -> Optional[list[VoiceStateModel]]:
        return self._model.voice_states

    @property
    def welcome_screen(self) -> Optional[WelcomeScreenModel]:
        return self._model.welcome_screen

    @property
    def widget_channel_id(self) -> Optional[Snowflake]:
        return self._model.widget_channel_id

    @property
    def widget_enabled(self) -> Optional[bool]:
        return self._model.widget_enabled
