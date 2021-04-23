from dippy.core.enums import StickerFormatType
from dippy.core.models.model import DippyCoreModel
from dippy.core.snowflake import Snowflake
from pydantic import validator
from typing import Optional


class StickerModel(DippyCoreModel):
    id: Snowflake
    pack_id: Snowflake
    name: str
    description: str
    tags: Optional[list[str]]
    asset: str
    format_type: StickerFormatType

    @validator("tags", pre=True)
    def create_tag_list(cls, value):
        return value.split(",") if value else []
