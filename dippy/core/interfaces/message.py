from __future__ import annotations
from dippy.core.caching.cacheable import Cacheable
from dippy.core.models.message import *
from dippy.core.timestamp import Timestamp
from gully import Gully


class Message(Cacheable):
    def __init__(self, model: MessageModel):
        self._model = model
        self._change_event_stream = Gully()

    def update(self, model: MessageModel):
        self._model = self._model.copy(update=model.dict(exclude_unset=True))

    def freeze(self) -> Message:
        return Message(self._model)

    @property
    def created(self) -> Timestamp:
        return self._model.created

    @property
    def id(self) -> Optional[Snowflake]:
        return self._model.id

    @property
    def channel_id(self) -> Snowflake:
        return self._model.channel_id

    @property
    def guild_id(self) -> Optional[Snowflake]:
        return self._model.guild_id

    @property
    def author(self) -> Optional[UserModel]:
        return self._model.author

    @property
    def member(self) -> Optional[MemberModel]:
        return self._model.member

    @property
    def content(self) -> Optional[str]:
        return self._model.content

    @property
    def timestamp(self) -> Optional[datetime]:
        return self._model.timestamp

    @property
    def edited_timestamp(self) -> Optional[datetime]:
        return self._model.edited_timestamp

    @property
    def tts(self) -> Optional[bool]:
        return self._model.tts

    @property
    def mention_everyone(self) -> Optional[bool]:
        return self._model.mention_everyone

    @property
    def mentions(self) -> Optional[list[UserModel]]:
        return self._model.mentions

    @property
    def mention_roles(self) -> Optional[list[Snowflake]]:
        return self._model.mention_roles

    @property
    def mention_channels(self) -> Optional[list[ChannelMentionModel]]:
        return self._model.mention_channels

    @property
    def attachments(self) -> Optional[list[AttachmentModel]]:
        return self._model.attachments

    @property
    def embeds(self) -> Optional[list[EmbedModel]]:
        return self._model.embeds

    @property
    def reactions(self) -> Optional[list[ReactionModel]]:
        return self._model.reactions

    @property
    def nonce(self) -> Optional[Union[int, str]]:
        return self._model.nonce

    @property
    def pinned(self) -> Optional[bool]:
        return self._model.pinned

    @property
    def webhook_id(self) -> Optional[Snowflake]:
        return self._model.webhook_id

    @property
    def type(self) -> Optional[MessageType]:
        return self._model.type

    @property
    def activity(self) -> Optional[MessageActivityModel]:
        return self._model.activity

    @property
    def message_reference(self) -> Optional[MessageReferenceModel]:
        return self._model.message_reference

    @property
    def flags(self) -> Optional[int]:
        return self._model.flags

    @property
    def stickers(self) -> Optional[list[StickerModel]]:
        return self._model.stickers

    @property
    def referenced_message(self) -> Optional[MessageModel]:
        return self._model.referenced_message

    @property
    def interaction(self) -> Optional[MessageInteractionModel]:
        return self._model.interaction
