from dippy.core.models.model import DippyCoreModel
from dippy.core.models.role import RoleModel
from dippy.core.models.user import UserModel
from dippy.core.snowflake import Snowflake
from typing import Optional


class EmojiModel(DippyCoreModel):
    id: Optional[Snowflake]
    name: str
    roles: Optional[list[RoleModel]]
    user: Optional[UserModel]
    require_colons: Optional[bool]
    managed: Optional[bool]
    animated: Optional[bool]
    available: Optional[bool]
