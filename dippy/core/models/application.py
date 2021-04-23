from __future__ import annotations
from dippy.core.enums import ApplicationCommandOptionType
from dippy.core.models.model import DippyCoreModel
from dippy.core.models.team import TeamModel
from dippy.core.models.user import UserModel
from dippy.core.snowflake import Snowflake
from pydantic import Field
from typing import Optional, Union


class ApplicationModel(DippyCoreModel):
    bot_public: bool
    bot_require_code_grant: bool
    cover_image: Optional[str]
    description: str
    flags: int
    guild_id: Optional[Snowflake]
    icon: Optional[str]
    id: Snowflake
    name: str
    owner: UserModel
    primary_sku_id: Optional[Snowflake]
    privacy_policy_url: Optional[str]
    rpc_origins: Optional[list[str]]
    slug: Optional[str]
    summary: str
    team: Optional[TeamModel]
    terms_of_service_url: Optional[str]
    verify_key: str


class ApplicationCommandOptionChoiceModel(DippyCoreModel):
    name: str
    vale: Union[str, int]


class ApplicationCommandOptionModel(DippyCoreModel):
    type: ApplicationCommandOptionType
    name: str
    description: str
    required: bool = Field(default=False)
    choices: list[ApplicationCommandOptionChoiceModel] = Field(default_factory=list)
    options: list[ApplicationCommandOptionModel]


class ApplicationCommandModel(DippyCoreModel):
    id: Snowflake
    guild_id: Optional[Snowflake]
    application_id: Snowflake
    name: str
    description: str
    options: Optional[list[ApplicationCommandOptionModel]]
    default_permissions: bool = Field(default=True)
