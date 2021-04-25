from __future__ import annotations
from dippy.core.caching.cacheable import Cacheable
from dippy.core.models.channel import *
from dippy.core.timestamp import Timestamp
from gully import Gully


class Channel(Cacheable):
    def __init__(self, model: ChannelModel):
        self._model = model
        self._change_event_stream = Gully()

    def update(self, model: ChannelModel):
        self._model = self._model.copy(update=model.dict(exclude_unset=True))

    def freeze(self) -> Channel:
        return Channel(self._model)

    @property
    def created(self) -> Timestamp:
        return self._model.created

    @property
    def id(self) -> Snowflake:
        return self._model.id

    @property
    def type(self) -> ChannelType:
        return self._model.type

    @property
    def application_id(self) -> Optional[Snowflake]:
        return self._model.application_id

    @property
    def bitrate(self) -> Optional[int]:
        return self._model.bitrate

    @property
    def created_at(self) -> Optional[datetime]:
        return self._model.created_at

    @property
    def guild_id(self) -> Optional[Snowflake]:
        return self._model.guild_id

    @property
    def icon(self) -> Optional[str]:
        return self._model.icon

    @property
    def last_message_id(self) -> Optional[Snowflake]:
        return self._model.last_message_id

    @property
    def last_pin_timestamp(self) -> Optional[datetime]:
        return self._model.last_pin_timestamp

    @property
    def name(self) -> Optional[str]:
        return self._model.name

    @property
    def nsfw(self) -> Optional[bool]:
        return self._model.nsfw

    @property
    def owner_id(self) -> Optional[Snowflake]:
        return self._model.owner_id

    @property
    def parent_id(self) -> Optional[Snowflake]:
        return self._model.parent_id

    @property
    def permission_overwrites(self) -> list[OverwriteModel]:
        return self._model.permission_overwrites

    @property
    def position(self) -> Optional[int]:
        return self._model.position

    @property
    def rate_limit_per_user(self) -> Optional[int]:
        return self._model.rate_limit_per_user

    @property
    def recipients(self) -> Optional[list[UserModel]]:
        return self._model.recipients

    @property
    def rtc_region(self) -> Optional[str]:
        return self._model.rtc_region

    @property
    def topic(self) -> Optional[str]:
        return self._model.topic

    @property
    def user_limit(self) -> Optional[int]:
        return self._model.user_limit

    @property
    def video_quality_mode(self) -> Optional[int]:
        return self._model.video_quality_mode
