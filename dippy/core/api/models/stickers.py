from __future__ import annotations as _
from dippy.core.enums.stickers import StickerType, StickerFormatType
from dippy.core.api.models.users import User
from dippy.core.model.models import Model
from dippy.core.snowflake import Snowflake
from typing import Optional


class Sticker(Model):
    id: Snowflake
    pack_id: Optional[Snowflake]
    name: str
    description: Optional[str]
    tags: str
    type: StickerType
    format_type: StickerFormatType
    available: Optional[bool]
    guild_id: Optional[Snowflake]
    user: Optional[User]
    sort_value: Optional[int]
