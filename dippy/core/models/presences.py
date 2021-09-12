from attr import attrs
from typing import Optional
from dippy.core.enums.users import Status
from dippy.core.models.activity import Activity
from dippy.core.models.users import User
from dippy.core.snowflake import Snowflake


@attrs(auto_attribs=True)
class ClientStatus:
    desktop: Optional[str]
    mobile: Optional[str]
    web: Optional[str]


@attrs(auto_attribs=True)
class Presence:
    user: User
    guild_id: Snowflake
    status: Status
    activities: list[Activity]
    client_status: ClientStatus
