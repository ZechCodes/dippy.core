from __future__ import annotations as _
from dippy.core.datetime_helpers import datetime
from dippy.core.enums.activity import ActivityFlag, ActivityType
from dippy.core.model.models import Model
from dippy.core.snowflake import Snowflake
from typing import Optional


class Activity(Model):
    name: str
    type: ActivityType
    url: Optional[str]
    created_at: datetime
    timestamps: Optional[ActivityTimestamp]
    application_id: Optional[Snowflake]
    details: Optional[str]
    state: Optional[str]
    emoji: Optional[ActivityEmoji]
    party: Optional[ActivityParty]
    assets: Optional[ActivityAssets]
    secrets: Optional[ActivitySecrets]
    instance: Optional[bool]
    flags: Optional[ActivityFlag]
    buttons: Optional[list[ActivityButton]]


class ActivityAssets(Model):
    large_image: Optional[str]
    large_text: Optional[str]
    small_image: Optional[str]


class ActivityButton(Model):
    label: str
    url: str


class ActivityEmoji(Model):
    name: str
    id: Optional[Snowflake]
    animated: Optional[bool]


class ActivityParty(Model):
    id: Optional[str]
    size: Optional[list[int]]


class ActivitySecrets(Model):
    join: Optional[str]
    spectate: Optional[str]
    match: Optional[str]


class ActivityTimestamp(Model):
    start: Optional[datetime]
    end: Optional[datetime]
