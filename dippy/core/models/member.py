from datetime import datetime
from dippy.core.models.model import DippyCoreCacheableModel
from dippy.core.models.user import UserModel
from dippy.core.snowflake import Snowflake
from pydantic import Field
from typing import Optional


class MemberModel(DippyCoreCacheableModel):
    deaf: bool
    joined_at: datetime
    mute: bool
    roles: list[Snowflake]

    guild_id: Optional[Snowflake]
    hoisted_role: Optional[Snowflake]
    nick: Optional[str]
    pending: Optional[bool] = Field(alias="is_pending")
    permissions: Optional[str]
    premium_since: Optional[datetime]
    user: Optional[UserModel]

    @property
    def id(self) -> Optional[int]:
        if self.user:
            return self.user.id
        return
