from dippy.core.models.model import DippyCoreModel
from dippy.core.snowflake import Snowflake
from typing import Optional


class UserModel(DippyCoreModel):
    avatar: Optional[str]
    bot: Optional[bool]
    discriminator: str
    id: Snowflake
    username: str
