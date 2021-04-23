from __future__ import annotations
from dippy.core.enums import ApplicationCommandOptionType, InteractionType
from dippy.core.models.member import MemberModel
from dippy.core.models.model import DippyCoreModel
from dippy.core.models.user import UserModel
from dippy.core.snowflake import Snowflake
from pydantic import Field
from typing import Optional


class ApplicationCommandInteractionDataResolvedModel(DippyCoreModel):
    users: Optional[str]
    members: Optional[str]
    roles: Optional[str]
    channels: Optional[str]


class ApplicationCommandInteractionDataOptionModel(DippyCoreModel):
    name: str
    type: ApplicationCommandOptionType
    value: Optional[int]
    options: list[ApplicationCommandInteractionDataOptionModel] = Field(
        default_factory=list
    )


class ApplicationCommandInteractionDataModel(DippyCoreModel):
    id: Snowflake
    name: str
    resolved: Optional[ApplicationCommandInteractionDataResolvedModel]
    options: list[ApplicationCommandInteractionDataOptionModel] = Field(
        default_factory=list
    )


class InteractionModel(DippyCoreModel):
    id: Snowflake
    application_id: Snowflake
    type: InteractionType
    data: Optional[ApplicationCommandInteractionDataModel]
    guild_id: Optional[Snowflake]
    channel_id: Optional[Snowflake]
    member: Optional[MemberModel]
    user: Optional[UserModel]
    token: str
    version: int
