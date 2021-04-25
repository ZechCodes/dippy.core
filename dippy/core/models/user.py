from dippy.core.enums import UserFlag
from dippy.core.models.model import DippyCoreCacheableModel
from dippy.core.snowflake import Snowflake
from typing import Optional


class UserModel(DippyCoreCacheableModel):
    id: Snowflake
    username: str
    discriminator: str
    avatar: Optional[str]
    bot: Optional[bool]
    system: Optional[bool]
    mfa_enabled: Optional[bool]
    locale: Optional[str]
    verified: Optional[bool]
    email: Optional[str]
    flags: Optional[UserFlag]
