from __future__ import annotations
from typing import Optional
from dippy.core.api.models.users import User
from dippy.core.datetime_helpers import datetime
from dippy.core.enums.integrations import IntegrationExpireBehaviors
from dippy.core.model.models import Model
from dippy.core.snowflake import Snowflake


class IntegrationAccount(Model):
    id: str
    name: str


class IntegrationApplication(Model):
    id: Snowflake
    name: str
    icon: Optional[str]
    description: str
    summary: str
    bot: Optional[User]


class Integration(Model):
    id: Snowflake
    name: str
    type: str
    enabled: bool
    syncing: Optional[bool]
    role_id: Optional[Snowflake]
    enable_emoticons: Optional[bool]
    expire_behaviour: Optional[IntegrationExpireBehaviors]
    expire_grace_period: Optional[int]
    user: Optional[User]
    account: IntegrationAccount
    synced_at: Optional[datetime]
    subscriber_count: Optional[int]
    revoked: Optional[bool]
    application: Optional[IntegrationApplication]
