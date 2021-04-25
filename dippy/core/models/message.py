from __future__ import annotations
from datetime import datetime
from dippy.core.enums import (
    AllowedMention,
    InteractionResponseType,
    MessageActivityType,
    MessageType,
)
from dippy.core.models.attachment import AttachmentModel
from dippy.core.models.channel import ChannelMentionModel
from dippy.core.models.embed import EmbedModel
from dippy.core.models.member import MemberModel
from dippy.core.models.model import DippyCoreModel, DippyCoreCacheableModel
from dippy.core.models.reaction import ReactionModel
from dippy.core.models.sticker import StickerModel
from dippy.core.models.user import UserModel
from dippy.core.snowflake import Snowflake
from pydantic import Field
from typing import Optional, Union


class AllowedMentions(DippyCoreModel):
    parse: list[AllowedMention] = Field(default_factory=list)
    roles: list[Snowflake] = Field(default_factory=list, max_items=100)
    users: list[Snowflake] = Field(default_factory=list, max_items=100)
    replied_user: bool = Field(default=False)


class MessageActivityModel(DippyCoreModel):
    type: MessageActivityType
    party_id: Optional[str]


class MessageReferenceModel(DippyCoreModel):
    message_id: Optional[Snowflake]
    channel_id: Optional[Snowflake]
    guild_id: Optional[Snowflake]
    fail_if_not_exists: Optional[bool] = Field(default=True)


class MessageInteractionModel(DippyCoreModel):
    id: Snowflake
    type: InteractionResponseType
    name: str
    user: UserModel


class MessageModel(DippyCoreCacheableModel):
    id: Optional[Snowflake]
    channel_id: Snowflake
    guild_id: Optional[Snowflake]
    author: Optional[UserModel]
    member: Optional[MemberModel]
    content: Optional[str]
    timestamp: Optional[datetime]
    edited_timestamp: Optional[datetime]
    tts: Optional[bool]
    mention_everyone: Optional[bool]
    mentions: Optional[list[UserModel]]
    mention_roles: Optional[list[Snowflake]]
    mention_channels: Optional[list[ChannelMentionModel]]
    attachments: Optional[list[AttachmentModel]]
    embeds: Optional[list[EmbedModel]]
    reactions: Optional[list[ReactionModel]]
    nonce: Optional[Union[int, str]]
    pinned: Optional[bool]
    webhook_id: Optional[Snowflake]
    type: Optional[MessageType]
    activity: Optional[MessageActivityModel]
    message_reference: Optional[MessageReferenceModel]
    flags: Optional[int]
    stickers: Optional[list[StickerModel]]
    referenced_message: Optional[MessageModel]
    interaction: Optional[MessageInteractionModel]


MessageModel.update_forward_refs()
