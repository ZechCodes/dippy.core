from dippy.core.models.model import DippyCoreCacheableModel
from dippy.core.models.role import RoleModel
from dippy.core.models.user import UserModel
from dippy.core.snowflake import Snowflake
from typing import Optional


class EmojiModel(DippyCoreCacheableModel):
    name: str

    animated: Optional[bool]
    available: Optional[bool]
    id: Optional[Snowflake]
    managed: Optional[bool]
    require_colons: Optional[bool]
    roles: Optional[list[RoleModel]]
    user: Optional[UserModel]
