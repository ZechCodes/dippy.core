from datetime import datetime
from dippy.core.models.model import DippyCoreModel
from dippy.core.models.user import UserModel
from dippy.core.snowflake import Snowflake
from typing import Optional


class MemberModel(DippyCoreModel):
    guild_id: Optional[Snowflake]
    user: Optional[UserModel]
    nick: Optional[str]
    roles: list[Snowflake]
    joined_at: datetime
    premium_since: Optional[datetime]
    deaf: bool
    mute: bool
    is_pending: Optional[bool]
    hoisted_role: Optional[Snowflake]
