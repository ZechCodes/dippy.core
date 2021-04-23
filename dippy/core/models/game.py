from datetime import datetime
from dippy.core.models.model import DippyCoreModel
from dippy.core.snowflake import Snowflake


class GameModel(DippyCoreModel):
    created_at: datetime
    id: Snowflake
    name: str
    type: int
