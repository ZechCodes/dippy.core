from __future__ import annotations
from dippy.core.caching.cacheable import Cacheable
from dippy.core.models.user import *
from dippy.core.timestamp import Timestamp
from gully import Gully


class User(Cacheable):
    def __init__(self, model: UserModel):
        self._model = model
        self._change_event_stream = Gully()

    def update(self, model: UserModel):
        self._model = self._model.copy(update=model.dict(exclude_unset=True))

    def freeze(self) -> User:
        return User(self._model)

    @property
    def created(self) -> Timestamp:
        return self._model.created

    @property
    def id(self) -> Snowflake:
        return self._model.id

    @property
    def username(self) -> str:
        return self._model.username

    @property
    def discriminator(self) -> str:
        return self._model.discriminator

    @property
    def avatar(self) -> Optional[str]:
        return self._model.avatar

    @property
    def bot(self) -> Optional[bool]:
        return self._model.bot

    @property
    def system(self) -> Optional[bool]:
        return self._model.system

    @property
    def mfa_enabled(self) -> Optional[bool]:
        return self._model.mfa_enabled

    @property
    def locale(self) -> Optional[str]:
        return self._model.locale

    @property
    def verified(self) -> Optional[bool]:
        return self._model.verified

    @property
    def email(self) -> Optional[str]:
        return self._model.email

    @property
    def flags(self) -> Optional[UserFlag]:
        return self._model.flags
