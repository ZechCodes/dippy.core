from dippy.core.models.model import DippyCoreModel
from dippy.core.snowflake import Snowflake
from typing import Optional


class AttachmentModel(DippyCoreModel):
    id: Snowflake
    file: Optional[str]
    content_type: Optional[str]
    size: int
    url: str
    proxy_url: str
    height: Optional[int]
    width: Optional[int]
