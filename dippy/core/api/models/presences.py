from __future__ import annotations
from typing import Optional
from dippy.core.enums.users import Status
from dippy.core.api.models.activity import Activity
from dippy.core.api.models.users import User
from dippy.core.model.models import Model
from dippy.core.snowflake import Snowflake


class ClientStatus(Model):
    desktop: Optional[str]
    mobile: Optional[str]
    web: Optional[str]


class Presence(Model):
    user: User
    guild_id: Snowflake
    status: Status
    activities: list[Activity]
    client_status: ClientStatus
