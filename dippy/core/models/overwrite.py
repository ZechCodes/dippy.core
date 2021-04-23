from dippy.core.enums import OverwriteType
from dippy.core.models.model import DippyCoreModel
from dippy.core.snowflake import Snowflake


class OverwriteModel(DippyCoreModel):
    id: Snowflake
    type: OverwriteType
    deny_new: int
    deny: int
    allow_new: int
    allow: int
