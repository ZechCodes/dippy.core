from dippy.core.models.model import DippyCoreModel
from dippy.core.snowflake import Snowflake
from typing import Optional


class RoleTagsModel(DippyCoreModel):
    bot_id: Optional[Snowflake]
    integration_id: Optional[Snowflake]
    premium_subscriber: Optional[bool]


class RoleModel(DippyCoreModel):
    id: Snowflake
    name: str
    color: int
    hoist: bool
    position: int
    permissions: int
    managed: bool
    mentionable: bool
    tags: Optional[RoleTagsModel]
