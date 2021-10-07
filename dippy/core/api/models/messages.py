from dippy.core.api.models.emoji import Emoji
from dippy.core.datetime_helpers import datetime, from_timestamp
from dippy.core.enums.messages import EmbedType, AllowedMentionsType
from dippy.core.model.fields import Field
from dippy.core.model.models import Model
from dippy.core.snowflake import Snowflake
from typing import Optional


class MessageReference(Model):
    message_id: Optional[Snowflake]
    channel_id: Optional[Snowflake]
    guild_id: Optional[Snowflake]
    fail_if_not_exists: Optional[bool]


class FollowedChannel(Model):
    channel_id: Snowflake
    webhook_id: Snowflake


class Reaction(Model):
    count: int
    me: bool
    emoji: Emoji


class Overwrite(Model):
    id: Snowflake
    type: int
    allow: str
    deny: str


class ThreadMetadata(Model):
    archived: bool
    auto_archive_duration: int
    archive_timestamp: datetime = Field(converter=from_timestamp)
    locked: bool
    invitable: Optional[bool]


class ThreadMember(Model):
    id: Optional[Snowflake]
    user_id: Optional[Snowflake]
    join_timestamp: datetime = Field(converter=from_timestamp)
    flags: int


class EmbedAsset(Model):
    url: Optional[str]
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]


class EmbedProvider(Model):
    name: Optional[str]
    url: Optional[str]


class EmbedAuthor(Model):
    url: Optional[str]
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]
    name: Optional[str] = Field(validator=lambda inst, attr, value: len(value) <= 256)


class EmbedFooter(Model):
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]
    text: Optional[str] = Field(validator=lambda inst, attr, value: len(value) <= 2048)


class EmbedField(Model):
    name: str = Field(validator=lambda inst, attr, value: len(value) <= 256)
    value: str = Field(validator=lambda inst, attr, value: len(value) <= 1024)
    inline: Optional[bool] = False


class Embed(Model):
    url: Optional[str]
    color: Optional[int]
    footer: Optional[EmbedFooter]
    image: Optional[EmbedAsset]
    thumbnail: Optional[EmbedAsset]
    video: Optional[EmbedAsset]
    provider: Optional[EmbedProvider]
    author: Optional[EmbedAuthor]
    timestamp: Optional[datetime] = Field(converter=from_timestamp)
    title: Optional[str] = Field(validator=lambda inst, attr, value: len(value) <= 256)
    description: Optional[str] = Field(
        validator=lambda inst, attr, value: len(value) <= 4096
    )
    fields: Optional[list[EmbedField]] = Field(
        validator=lambda inst, attr, value: len(list[EmbedField]) <= 25
    )
    type: Optional[EmbedType] = EmbedType.RICH


class Attachment(Model):
    id: Snowflake
    filename: str
    content_type: Optional[str]
    size: int
    url: str
    proxy_url: str
    height: Optional[int]
    width: Optional[int]


class ChannelMention(Model):
    id: Snowflake
    guild_id: Snowflake
    type: int
    name: str


class AllowedMentions(Model):
    parse: list[AllowedMentionsType]
    roles: list[Snowflake]
    users: list[Snowflake]
    replied_user: bool


class Message(Model):
    ...
