from dippy.core.models.base_model import BaseModel
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


class Guild(BaseModel):
    ...
