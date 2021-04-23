from dippy.core.models.model import DippyCoreModel
from dippy.core.models.team_member import TeamMemberModel
from dippy.core.snowflake import Snowflake
from typing import Optional


class TeamModel(DippyCoreModel):
    icon: Optional[str]
    id: str
    members: list[TeamMemberModel]
    owner_user_id: Snowflake
