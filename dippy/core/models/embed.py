from datetime import datetime
from dippy.core.models.model import DippyCoreModel
from dippy.core.enums import EmbedType
from typing import Optional


class EmbedAssetModel(DippyCoreModel):
    url: Optional[str]
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]


class EmbedProviderModel(DippyCoreModel):
    url: Optional[str]
    name: Optional[str]


class EmbedAuthorModel(EmbedProviderModel):
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]


class EmbedFooterModel(DippyCoreModel):
    text: str
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]


class EmbedFieldModel(DippyCoreModel):
    title: str = Field(alias="name")
    contents: str = Field(alias="value")
    inline: Optional[bool]


class EmbedModel(DippyCoreModel):
    title: Optional[str]
    type: Optional[EmbedType]
    description: Optional[str]
    url: Optional[str]
    timestamp: Optional[datetime]
    color: Optional[int]
    footer: Optional[EmbedFooterModel]
    image: Optional[EmbedAssetModel]
    thumbnail: Optional[EmbedAssetModel]
    video: Optional[EmbedAssetModel]
    provider: Optional[EmbedProviderModel]
    author: Optional[EmbedAuthorModel]
    fields: Optional[list[EmbedFieldModel]]
