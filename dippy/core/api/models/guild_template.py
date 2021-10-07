from __future__ import annotations
from typing import Optional
from dippy.core.api.models.guilds import Guild
from dippy.core.api.models.users import User
from dippy.core.datetime_helpers import datetime
from dippy.core.model.models import Model
from dippy.core.snowflake import Snowflake


class GuildTemplate(Model):
    code: str
    name: str
    description: Optional[str]
    usage_count: int
    creator_id: Snowflake
    creator: User
    created_at: datetime
    updated_at: datetime
    source_guild_id: Snowflake
    serialized_source_guild: Guild
    is_dirty: Optional[bool]
