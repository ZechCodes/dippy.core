from abc import ABC, abstractmethod
from aiohttp import ClientSession
from bevy import Injectable
from dippy.core.gateway.bases import BaseGatewayConnection
from typing import Optional


class BaseDiscordAPI(ABC, Injectable):
    @property
    @abstractmethod
    def gateway(self) -> Optional[BaseGatewayConnection]:
        ...

    @property
    @abstractmethod
    def session(self) -> ClientSession:
        ...

    @abstractmethod
    async def close(self):
        ...

    @abstractmethod
    async def connect(self):
        ...
