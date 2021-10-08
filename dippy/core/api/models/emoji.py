from __future__ import annotations
from dippy.core.api.models.users import User
from dippy.core.model.models import Model
from dippy.core.snowflake import Snowflake
from typing import Optional


class Emoji(Model):
    id: Optional[Snowflake]
    name: Optional[str]
    roles: Optional[list[Snowflake]]
    user: Optional[User]
    require_colons: Optional[bool]
    managed: Optional[bool]
    animated: Optional[bool]
    available: Optional[bool]
