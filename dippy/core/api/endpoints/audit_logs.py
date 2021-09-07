from __future__ import annotations
from dippy.core.api.request import request_model, query_arg, url_arg
from dippy.core.enums.audit_logs import AuditLogEvents
from dippy.core.snowflake import Snowflake
from typing import Optional


@request_model
class GetAuditLogRequest:
    endpoint = "/guilds/{guild_id}/audit-logs"
    method = "GET"

    guild_id: Snowflake = url_arg()

    user_id: Optional[Snowflake] = query_arg()
    action_type: Optional[AuditLogEvents] = query_arg()
    before: Optional[Snowflake] = query_arg()
    limit: Optional[int] = query_arg()
