from __future__ import annotations
from dippy.core.model.models import Model
from dippy.core.snowflake import Snowflake


class Application(Model):
    id: Snowflake
