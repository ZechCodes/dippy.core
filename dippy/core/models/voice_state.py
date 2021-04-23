from datetime import datetime
from dippy.core.models.member import MemberModel
from dippy.core.models.model import DippyCoreModel
from dippy.core.snowflake import Snowflake
from typing import Optional


class VoiceStateModel(DippyCoreModel):
    guild_id: Optional[Snowflake]
    channel_id: Optional[Snowflake]
    user_id: Snowflake
    member: Optional[MemberModel]
    session_id: str
    deaf: bool
    mute: bool
    self_deaf: bool
    self_mute: bool
    self_stream: Optional[bool]
    self_video: bool
    suppress: bool
    request_to_speak_timestamp: Optional[datetime]
