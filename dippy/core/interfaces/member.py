from __future__ import annotations
from dippy.core.caching.cacheable import Cacheable
from dippy.core.models.member import *
from dippy.core.interfaces.user import User
from dippy.core.timestamp import Timestamp
from gully import Gully


class Member(Cacheable):
    def __init__(self, model: MemberModel, user: User):
        self._model = model
        self._user = user
        self._change_event_stream = Gully()

    def update(self, model: MemberModel):
        self._model = self._model.copy(update=model.dict(exclude_unset=True))
        if model.user:
            self._user.update(model.user)

    def freeze(self) -> Member:
        user = self.user.freeze()
        return Member(self._model, user)

    @property
    def created(self) -> Timestamp:
        return self._model.created

    @property
    def id(self) -> Optional[Snowflake]:
        return self.user.id

    @property
    def deaf(self) -> bool:
        return self._model.deaf

    @property
    def joined_at(self) -> datetime:
        return self._model.joined_at

    @property
    def mute(self) -> bool:
        return self._model.mute

    @property
    def roles(self) -> list[Snowflake]:
        return self._model.roles

    @property
    def guild_id(self) -> Optional[Snowflake]:
        return self._model.guild_id

    @property
    def hoisted_role(self) -> Optional[Snowflake]:
        return self._model.hoisted_role

    @property
    def nick(self) -> Optional[str]:
        return self._model.nick

    @property
    def pending(self) -> Optional[bool]:
        return self._model.pending

    @property
    def permissions(self) -> Optional[str]:
        return self._model.permissions

    @property
    def premium_since(self) -> Optional[datetime]:
        return self._model.premium_since

    @property
    def user(self) -> User:
        return self._user
