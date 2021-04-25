from __future__ import annotations
from abc import ABC, abstractmethod
from bevy import Injectable
from dippy.core.caching.cache import Cache
import dippy.core.interfaces.channel
import dippy.core.interfaces.guild
import dippy.core.interfaces.member
import dippy.core.interfaces.message
import dippy.core.interfaces.user


class BaseCacheManager(ABC, Injectable):
    @property
    @abstractmethod
    def channels(self) -> Cache[dippy.core.interfaces.channel.Channel]:
        ...

    @property
    @abstractmethod
    def guilds(self) -> Cache[dippy.core.interfaces.guild.Guild]:
        ...

    @property
    @abstractmethod
    def messages(self) -> Cache[dippy.core.interfaces.message.Message]:
        ...

    @property
    @abstractmethod
    def members(self) -> Cache[dippy.core.interfaces.member.Member]:
        ...

    @property
    @abstractmethod
    def users(self) -> Cache[dippy.core.interfaces.user.User]:
        ...
