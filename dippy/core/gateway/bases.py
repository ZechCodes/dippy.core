from abc import ABC, abstractmethod
from bevy import Injectable
from dippy.core.events import BaseEventStream
from dippy.core.gateway.payload import Payload
from typing import Optional


class BaseGatewayConnection(ABC, Injectable):
    @property
    @abstractmethod
    def connected(self) -> bool:
        ...

    @property
    @abstractmethod
    def gateway(self) -> str:
        ...

    @property
    @abstractmethod
    def sequence_index(self) -> Optional[int]:
        ...

    @abstractmethod
    async def connect(self):
        ...

    @abstractmethod
    async def disconnect(self, code: int = 1000):
        ...

    @abstractmethod
    async def resume(self):
        ...

    @abstractmethod
    async def send(self, payload: Payload):
        ...


class BaseHeartbeat(ABC, Injectable):
    @property
    @abstractmethod
    def running(self) -> bool:
        ...

    @abstractmethod
    def stop(self):
        ...
