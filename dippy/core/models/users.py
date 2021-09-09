from dippy.core.datetime_helpers import datetime
from dippy.core.models.base_model import BaseModel
from dippy.core.snowflake import Snowflake
from typing import Optional


class User(BaseModel):
    id: Snowflake
    username: str
    discriminator: str
    avatar: Optional[str]
    bot: Optional[bool]
    system: Optional[bool]
    mfa_enabled: Optional[bool]
    banner: Optional[str]
    accent_color: Optional[int]
    locale: Optional[str]
    verified: Optional[bool]
    email: Optional[str]
    flags: Optional[int]
    premium_type: Optional[int]
    public_flags: Optional[int]


class Member(BaseModel):
    user: Optional[User]
    nick: Optional[str]
    roles: list[Snowflake]
    joined_at: datetime
    premium_since: Optional[datetime]
    deaf: bool
    mute: bool
    pending: Optional[bool]
    permissions: Optional[str]
