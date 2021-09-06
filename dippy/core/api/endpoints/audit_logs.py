from __future__ import annotations
from dippy.core.api.request import converters, model, query_arg, url_arg
from dippy.core.enums.audit_logs import AuditLogEvents
from dippy.core.snowflake import Snowflake
from typing import Optional


@model
class GetAuditLogRequest:
    endpoint = "/guilds/{guild_id}/audit-logs"
    method = "GET"

    guild_id: Snowflake = url_arg(converter=Snowflake)

    user_id: Optional[Snowflake] = query_arg(
        converter=converters.default_if_none(Snowflake)
    )
    action_type: Optional[AuditLogEvents] = query_arg(
        converter=converters.default_if_none(AuditLogEvents)
    )
    before: Optional[Snowflake] = query_arg(
        converter=converters.default_if_none(Snowflake)
    )
    limit: Optional[int] = query_arg(converter=converters.default_if_none(int))
