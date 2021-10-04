from __future__ import annotations
from attr import attrs
from dippy.core.datetime_helpers import datetime
from dippy.core.enums.activity import ActivityFlag, ActivityType
from dippy.core.snowflake import Snowflake
from typing import Optional


@attrs(auto_attribs=True)
class Activity:
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


@attrs(auto_attribs=True)
class ActivityAssets:
    large_image: Optional[str]
    large_text: Optional[str]
    small_image: Optional[str]


@attrs(auto_attribs=True)
class ActivityButton:
    label: str
    url: str


@attrs(auto_attribs=True)
class ActivityEmoji:
    name: str
    id: Optional[Snowflake]
    animated: Optional[bool]


@attrs(auto_attribs=True)
class ActivityParty:
    id: Optional[str]
    size: Optional[list[int]]


@attrs(auto_attribs=True)
class ActivitySecrets:
    join: Optional[str]
    spectate: Optional[str]
    match: Optional[str]


@attrs(auto_attribs=True)
class ActivityTimestamp:
    start: Optional[datetime]
    end: Optional[datetime]
