from aiohttp import ClientSession
from bevy import Context, Injectable
from dippy.core.api.bases import BaseDiscordAPI
from dippy.core.gateway.bases import BaseGatewayConnection
from dippy.core.gateway.connection import GatewayConnection
from typing import Optional


class DiscordAPI(BaseDiscordAPI, Injectable):
    context: Context

    def __init__(self, token: str, **kwargs):
        self._token = token
        self._settings = kwargs

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    @property
    def gateway(self) -> Optional[BaseGatewayConnection]:
        return self.context.get(BaseGatewayConnection, default=None)

    @property
    def session(self) -> ClientSession:
        return self._session

    async def close(self):
        if self.gateway and self.gateway.connected:
            await self.gateway.disconnect()

        await self._session.close()

    def connect(self):
        if not self.gateway:
            gateway = self.context.create(
                GatewayConnection, self._token, **self._settings
            )
            self.context.add(gateway)
        return self.gateway.connect()
