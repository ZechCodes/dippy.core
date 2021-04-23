from dippy.core.enums import Status
from dippy.core.models.activity import ActivityModel
from dippy.core.models.client_status import ClientStatusModel
from dippy.core.models.game import GameModel
from dippy.core.models.model import DippyCoreModel
from dippy.core.snowflake import Snowflake
from pydantic import Field, validator
from typing import Optional


class PresenceModel(DippyCoreModel):
    user_id: Snowflake = Field(alias="user")
    status: Status
    game: Optional[GameModel]
    client_status: ClientStatusModel
    activities: list[ActivityModel]

    @validator("user_id", pre=True)
    def get_user_id(cls, value):
        return Snowflake(value.get("id"))
