from datetime import datetime
from dippy.core.models.model import DippyCoreModel
from dippy.core.snowflake import Snowflake
from typing import Union


class GameModel(DippyCoreModel):
    created_at: datetime
    id: Union[Snowflake, str]
    name: str
    type: int
