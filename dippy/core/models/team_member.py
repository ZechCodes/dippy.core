from dippy.core.enums import MembershipState
from dippy.core.models.model import DippyCoreModel
from dippy.core.models.user import UserModel
from dippy.core.snowflake import Snowflake


class TeamMemberModel(DippyCoreModel):
    membership_state: MembershipState
    permissions: list[str]
    team_id: Snowflake
    user: UserModel
