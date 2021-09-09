from attr import attrs, attrib

from dippy.core.api.request import json_arg
from dippy.core.enums.messages import EmbedType, AllowedMentionsType
from dippy.core.datetime_helpers import datetime, from_timestamp
from typing import Optional

from dippy.core.snowflake import Snowflake


@attrs(auto_attribs=True)
class Overwrite:
    id: Snowflake
    type: int
    allow: str
    deny: str


@attrs(auto_attribs=True)
class ThreadMetadata:
    archived: bool
    auto_archive_duration: int
    archive_timestamp: datetime = attrib(converter=from_timestamp)
    locked: bool
    invitable: Optional[bool]


@attrs(auto_attribs=True)
class ThreadMember:
    id: Optional[Snowflake]
    user_id: Optional[Snowflake]
    join_timestamp: datetime = attrib(converter=from_timestamp)
    flags: int


@attrs(auto_attribs=True)
class EmbedAsset:
    url: Optional[str]
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]


@attrs(auto_attribs=True)
class EmbedProvider:
    name: Optional[str]
    url: Optional[str]


@attrs(auto_attribs=True)
class EmbedAuthor:
    url: Optional[str]
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]
    name: Optional[str] = json_arg(validator=lambda inst, attr, value: len(value) <= 256)


@attrs(auto_attribs=True)
class EmbedFooter:
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]
    text: Optional[str] = json_arg(validator=lambda inst, attr, value: len(value) <= 2048)


@attrs(auto_attribs=True)
class EmbedField:
    name: str = json_arg(validator=lambda inst, attr, value: len(value) <= 256)
    value: str = json_arg(validator=lambda inst, attr, value: len(value) <= 1024)
    inline: Optional[bool] = False


@attrs(auto_attribs=True)
class Embed:
    url: Optional[str]
    color: Optional[int]
    footer: Optional[EmbedFooter]
    image: Optional[EmbedAsset]
    thumbnail: Optional[EmbedAsset]
    video: Optional[EmbedAsset]
    provider: Optional[EmbedProvider]
    author: Optional[EmbedAuthor]
    timestamp: Optional[datetime] = attrib(converter=from_timestamp)
    title: Optional[str] = json_arg(validator=lambda inst, attr, value: len(value) <= 256)
    description: Optional[str] = json_arg(validator=lambda inst, attr, value: len(value) <= 4096)
    fields: Optional[list[EmbedField]] = json_arg(validator=lambda inst, attr, value: len(list[EmbedField]) <= 25)
    type: Optional[EmbedType] = EmbedType.RICH


@attrs(auto_attribs=True)
class Attachment:
    id: Snowflake
    filename: str
    content_type: Optional[str]
    size: int
    url: str
    proxy_url: str
    height: Optional[int]
    width: Optional[int]


@attrs(auto_attribs=True)
class ChannelMention:
    id: Snowflake
    guild_id: Snowflake
    type: int
    name: str


@attrs(auto_attribs=True)
class AllowedMentions:
    parse: list[AllowedMentionsType]
    roles: list[Snowflake]
    users: list[Snowflake]
    replied_user: bool
