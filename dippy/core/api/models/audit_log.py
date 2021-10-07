from __future__ import annotations
from typing import Optional, Any
from dippy.core.api.models.base_model import Model
from dippy.core.api.models.channels import Channel
from dippy.core.api.models.integrations import Integration
from dippy.core.api.models.users import User
from dippy.core.api.models.webhooks import Webhook
from dippy.core.enums.audit_logs import AuditLogEvents
from dippy.core.snowflake import Snowflake


class AuditLogChange(Model):
    new_value: dict[str, Any]
    old_value: dict[str, Any]
    key: str


class OptionalAuditEntryInfo(Model):
    channel_id: Snowflake
    count: str
    delete_member_types: str
    id: Snowflake
    members_removed: str
    message_id: Snowflake
    role_name: str
    type: str


class AuditLogEntry(Model):
    target_id: Optional[str]
    changes: Optional[list[AuditLogChange]]
    user_id: Optional[Snowflake]
    id: Snowflake
    action_type: AuditLogEvents
    options: Optional[OptionalAuditEntryInfo]
    reason: Optional[str]


class AuditLog(Model):
    audit_log_entries: list[AuditLogEntry]
    integrations: list[Integration]
    threads: list[Channel]
    users: list[User]
    webhooks: list[Webhook]
