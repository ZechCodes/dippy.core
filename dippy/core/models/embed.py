from __future__ import annotations
from datetime import datetime
from dippy.core.models.model import DippyCoreModel
from dippy.core.enums import EmbedType
from pydantic import Field
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

    def add_field(self, title: str, contents: str, inline: bool = False) -> EmbedModel:
        if self.fields is None:
            self.fields = []

        self.fields.append(EmbedFieldModel(name=title, value=contents, inline=inline))
        return self

    def set_author(
        self,
        name: Optional[str] = None,
        url: Optional[str] = None,
        icon_url: Optional[int] = None,
        proxy_icon_url: Optional[str] = None,
    ) -> EmbedModel:
        self.author = EmbedAuthorModel(
            name=name, url=url, icon_url=icon_url, proxy_icon_url=proxy_icon_url
        )
        return self

    def set_footer(
        self,
        text: str,
        icon_url: Optional[str] = None,
        proxy_icon_url: Optional[str] = None,
    ) -> EmbedModel:
        self.footer = EmbedFooterModel(
            text=text, icon_url=icon_url, proxy_icon_url=proxy_icon_url
        )
        return self

    def set_image(
        self,
        url: Optional[str] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
        proxy_url: Optional[str] = None,
    ) -> EmbedModel:
        self.image = EmbedAssetModel(
            url=url, height=height, width=width, proxy_url=proxy_url
        )
        return self

    def set_provider(
        self, name: Optional[str] = None, url: Optional[str] = None
    ) -> EmbedModel:
        self.provider = EmbedProviderModel(name=name, url=url)
        return self

    def set_thumbnail(
        self,
        url: Optional[str] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
        proxy_url: Optional[str] = None,
    ) -> EmbedModel:
        self.thumbnail = EmbedAssetModel(
            url=url, height=height, width=width, proxy_url=proxy_url
        )
        return self

    def set_video(
        self,
        url: Optional[str] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
        proxy_url: Optional[str] = None,
    ) -> EmbedModel:
        self.video = EmbedAssetModel(
            url=url, height=height, width=width, proxy_url=proxy_url
        )
        return self
