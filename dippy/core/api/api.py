from aiohttp import ClientSession
from bevy import Context, Injectable
from dippy.core.api.bases import BaseDiscordAPI
from dippy.core.gateway.bases import BaseGatewayConnection
from dippy.core.gateway.connection import GatewayConnection
from typing import Optional
import logging


class DiscordAPI(BaseDiscordAPI, Injectable):
    context: Context

    def __init__(self, token: str, **kwargs):
        self._log = logging.getLogger().getChild("dippy.core")
        self._token = token
        self._settings = kwargs
        self._session: ClientSession = self._create_session()

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

    def _create_user_agent(self):
        from dippy.core.version import (
            __aiohttp_version__,
            __python_version__,
            __version__,
        )

        browser = self._settings.get("browser", "dippy.core")
        repo = "https://github.com/ZechCodes/dippy.core"
        return f"{browser} ({repo}, {__version__}), Python/{__python_version__}, aiohttp/{__aiohttp_version__}"

    def _create_session(self) -> ClientSession:
        user_agent = self._create_user_agent()
        self._log.info(f"Connecting as {user_agent!r}")
        return ClientSession(
            headers={
                "Authorization": f"Bot {self._token}",
                "User-Agent": user_agent,
                "X-Ratelimit-Precision": "millisecond",
            }
        )
