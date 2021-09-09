from attr import attrs, attrib
from dippy.core.enums.messages import EmbedType, AllowedMentionsType
from dippy.core.datetime_helpers import datetime, from_timestamp
from typing import Optional, List

from dippy.core.snowflake import Snowflake


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
    name: Optional[str]
    url: Optional[str]
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]


@attrs(auto_attribs=True)
class EmbedFooter:
    text: Optional[str]
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]


@attrs(auto_attribs=True)
class EmbedField:
    name: str
    value: str
    inline: Optional[bool] = False


@attrs(auto_attribs=True)
class Embed:
    title: Optional[str]
    description: Optional[str]
    url: Optional[str]
    color: Optional[int]
    footer: Optional[EmbedFooter]
    image: Optional[EmbedAsset]
    thumbnail: Optional[EmbedAsset]
    video: Optional[EmbedAsset]
    provider: Optional[EmbedProvider]
    author: Optional[EmbedAuthor]
    fields: Optional[list[EmbedField]]
    timestamp: Optional[datetime] = attrib(converter=from_timestamp)
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
    parse: List[AllowedMentionsType]
    roles: List[Snowflake]
    users: List[Snowflake]
    replied_user: bool
