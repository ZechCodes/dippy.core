from __future__ import annotations
from typing import Optional
from dippy.core.api.models.channels import Channel
from dippy.core.api.models.guilds import Guild
from dippy.core.api.models.users import User
from dippy.core.model.models import Model
from dippy.core.snowflake import Snowflake


class Webhook(Model):
    id: Snowflake
    type: int
    guild_id: Optional[Snowflake]
    channel_id: Optional[Snowflake]
    user: Optional[User]
    name: Optional[str]
    avatar: Optional[str]
    token: Optional[str]
    application_id: Optional[Snowflake]
    source_guild: Optional[Guild]
    source_channel: Optional[Channel]
    url: Optional[str]
