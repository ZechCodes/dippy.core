from dippy.core.enums import Status
from dippy.core.models.model import DippyCoreModel
from pydantic import Field


class ClientStatusModel(DippyCoreModel):
    mobile: Status = Field(default=Status.OFFLINE)
    desktop: Status = Field(default=Status.OFFLINE)
    web: Status = Field(default=Status.OFFLINE)
