from datetime import datetime
from dippy.core.enums import ActivityType
from dippy.core.models.model import DippyCoreModel
from dippy.core.snowflake import Snowflake
from pydantic import validator
from typing import Optional, Union


class ActivityTimestampsModel(DippyCoreModel):
    start: Optional[datetime]
    end: Optional[datetime]

    @validator("start", "end", pre=True)
    def datetime_from_unix_millisecond_timestamp(cls, value):
        return value if not value else datetime.utcfromtimestamp(int(value) / 1000)


class ActivityEmojiModel(DippyCoreModel):
    name: str
    id: Optional[Snowflake]
    animated: Optional[bool]


class ActivityPartyModel(DippyCoreModel):
    id: Optional[str]
    size: Optional[tuple[int, int]]


class ActivityAssetModel(DippyCoreModel):
    large_image: Optional[str]
    large_text: Optional[str]
    small_image: Optional[str]
    small_text: Optional[str]


class ActivitySecretModel(DippyCoreModel):
    join: Optional[str]
    spectate: Optional[str]
    match: Optional[str]


class ActivityButtonModel(DippyCoreModel):
    label: str
    url: str


class ActivityModel(DippyCoreModel):
    created_at: datetime
    id: Union[Snowflake, str]
    name: str
    type: ActivityType
    url: Optional[str]
    timestamps: Optional[ActivityTimestampsModel]
    application_id: Optional[Snowflake]
    details: Optional[str]
    state: Optional[str]
    emoji: Optional[ActivityEmojiModel]
    party: Optional[ActivityPartyModel]
    assets: Optional[ActivityAssetModel]
    secrets: Optional[ActivitySecretModel]
    instance: Optional[bool]
    flags: Optional[int]
    buttons: Optional[list[Union[ActivityButtonModel, str]]]
