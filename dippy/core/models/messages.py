from attr import attrs, attrib
from dippy.core.enums.messages import EmbedType
from dippy.core.datetime_helpers import datetime, from_timestamp
from typing import Optional


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
    url: Optional[datetime] = attrib(converter=from_timestamp)
    color: Optional[int]
    footer: Optional[EmbedFooter]
    image: Optional[EmbedAsset]
    thumbnail: Optional[EmbedAsset]
    video: Optional[EmbedAsset]
    provider: Optional[EmbedProvider]
    author: Optional[EmbedAuthor]
    fields: Optional[list[EmbedField]]
    type: Optional[EmbedType] = EmbedType.RICH
