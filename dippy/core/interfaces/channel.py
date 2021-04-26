from __future__ import annotations
from bevy import Factory, Injectable
from dippy.core.api.request import Request
from dippy.core.caching.cacheable import Cacheable
from dippy.core.interfaces.message import Message
from dippy.core.models.channel import *
from dippy.core.models.embed import EmbedModel
from dippy.core.models.message import (
    AllowedMentions,
    MessageModel,
    MessageReferenceModel,
)
from dippy.core.timestamp import Timestamp
from pydantic import BaseModel, Field
from gully import Gully
from pathlib import Path
from io import IOBase
from typing import Union
import dippy.core.caching.bases


FileName = FilePath = str
File = IOBase
FileUpload = Union[File, FilePath, Path]


class SendMessageModel(BaseModel):
    content: Optional[str] = Field(max_length=2000)
    tts: bool = Field(default=False)
    embed: Optional[EmbedModel]
    allowed_mentions: Optional[AllowedMentions]
    message_reference: Optional[MessageReferenceModel]


class Channel(Cacheable, Injectable):
    cache: dippy.core.caching.bases.BaseCacheManager
    request: Factory[Request]

    def __init__(self, model: ChannelModel):
        self._model = model
        self._change_event_stream = Gully()

    async def delete(self):
        await self.request(f"/channels/{self.id}").delete()

    def freeze(self) -> Channel:
        return Channel(self._model)

    async def retrieve_message(self, message_id: Snowflake) -> Message:
        response, _ = await self.request(
            f"/channels/{self.id}/messages/{message_id}"
        ).get()
        return self.cache.messages.add(MessageModel(**response))

    async def retrieve_messages(
        self,
        after: Optional[Message] = None,
        around: Optional[Message] = None,
        before: Optional[Message] = None,
        limit: Optional[int] = None,
    ) -> list[Message]:
        args = {}
        if after:
            args["after"] = after.id
        if around:
            args["around"] = around.id
        if before:
            args["before"] = before.id
        if limit is not None:
            args["limit"] = limit
        return await self.request(f"/channels/{self.id}/messages").get(**args)

    async def send(
        self,
        content: Optional[str] = None,
        embed: Optional[EmbedModel] = None,
        tts: bool = False,
        allowed_mentions: Optional[AllowedMentions] = None,
        message_reference: Optional[MessageReferenceModel] = None,
        files: Optional[dict[FileName, FileUpload]] = None,
    ):
        if not content and not embed:
            raise ValueError("You must provide either message content or an embed")

        message = SendMessageModel(
            content=content,
            embed=embed,
            tts=tts,
            allowed_mentions=allowed_mentions,
            message_reference=message_reference,
        )
        endpoint = self.request(f"/channels/{self.id}/messages")
        response = await endpoint.post(
            **message.dict(exclude_none=True), files=self._construct_files(files)
        )
        return self.cache.messages.add(MessageModel(**response))

    def update(self, model: ChannelModel):
        self._model = self._model.copy(update=model.dict(exclude_unset=True))

    def _construct_files(
        self, files: Optional[dict[FileName, FileUpload]]
    ) -> Optional[dict[FileName, File]]:
        if not files:
            return

        uploads = {}
        for filename, file in files.items():
            fp = file
            if isinstance(file, FilePath):
                fp = Path(file).resolve().open("rb")
            elif isinstance(file, Path):
                fp = file.resolve().open("rb")
            uploads[filename] = fp
        return uploads

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
