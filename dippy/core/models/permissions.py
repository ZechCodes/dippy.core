from attr import attrs
from typing import Optional
from dippy.core.enums.permissions import PermissionType
from dippy.core.snowflake import Snowflake


@attrs(auto_attribs=True)
class RoleTags:
    bot_id: Snowflake
    integration_id: Snowflake
    premium_subscriber: Optional


@attrs(auto_attribs=True)
class Role:
    id: Snowflake
    name: str
    color: int
    hoist: bool
    position: int
    permissions: str
    managed: bool
    mentionable: bool
    tags: Optional[RoleTags]


@attrs(auto_attribs=True)
class PermissionOverwrite:
    id: Snowflake
    type: PermissionType
    allow: str
    deny: str
