from attr import attrs
from typing import Optional

from dippy.core.models.permissions import Role
from dippy.core.models.user import User
from dippy.core.snowflake import Snowflake


@attrs(auto_attribs=True)
class Emoji:
    id: Optional[Snowflake]
    name: Optional[str]
    roles: Optional[list[Role.id]]
    user: Optional[User]
    require_colons: Optional[bool]
    managed: Optional[bool]
    animated: Optional[bool]
    available: Optional[bool]
