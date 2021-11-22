from __future__ import annotations
from dippy.core.api.request import RequestModel, QueryArgField, URLArgField
from dippy.core.enums.audit_logs import AuditLogEvents
from dippy.core.snowflake import Snowflake
from typing import Optional


class GetAuditLogRequest(RequestModel):
    endpoint = "/guilds/{guild_id}/audit-logs"
    method = "GET"

    guild_id: Snowflake = URLArgField()

    user_id: Optional[Snowflake] = QueryArgField()
    action_type: Optional[AuditLogEvents] = QueryArgField()
    before: Optional[Snowflake] = QueryArgField()
    limit: Optional[int] = QueryArgField()
