from attr import attrs
from dippy.core.models.users import User
from dippy.core.snowflake import Snowflake
from typing import Optional


@attrs(auto_attribs=True)
class Emoji:
    id: Optional[Snowflake]
    name: Optional[str]
    roles: Optional[list[Snowflake]]
    user: Optional[User]
    require_colons: Optional[bool]
    managed: Optional[bool]
    animated: Optional[bool]
    available: Optional[bool]
