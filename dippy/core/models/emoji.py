from __future__ import annotations
from dippy.core.models.model import DippyCoreCacheableModel
from dippy.core.models.role import RoleModel
from dippy.core.models.user import UserModel
from dippy.core.snowflake import Snowflake
from typing import Optional


class EmojiModel(DippyCoreCacheableModel):
    name: str

    animated: Optional[bool]
    available: Optional[bool]
    id: Optional[Snowflake]
    managed: Optional[bool]
    require_colons: Optional[bool]
    roles: Optional[list[RoleModel]]
    user: Optional[UserModel]

    def __str__(self):
        if self.id:
            return f"{self.name}:{self.id}"
        return self.name

    @classmethod
    def parse(cls, emoji: str) -> EmojiModel:
        if isinstance(emoji, cls):
            return emoji

        name, _, emoji_id = emoji.partition(":")
        return cls(name=name, id=int(emoji_id) if emoji_id else None)
