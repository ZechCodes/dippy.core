from bevy import Context, Injectable
from aiohttp import client_exceptions, ClientSession, ClientWebSocketResponse, WSMsgType
from dippy.core.api.bases import BaseDiscordAPI
from dippy.core.enums import GatewayCode, Event
from dippy.core.events import BaseEventStream
from dippy.core.gateway.bases import BaseGatewayConnection, BaseHeartbeat
from dippy.core.gateway.heartbeat import Heartbeat
from dippy.core.gateway.payload import Payload
from dippy.core.intents import Intents
from dippy.core.models.events import EventReady
from typing import Optional
import asyncio
import json
import logging
import random
import sys
import zlib


class GatewayConnection(BaseGatewayConnection, Injectable):
    __gateway_version__ = 8

    api: BaseDiscordAPI
    context: Context
    events: BaseEventStream
    loop: asyncio.AbstractEventLoop

    def __init__(self, token: str, **kwargs):
        self._connected = asyncio.Event()
        self._filters = {}
        self._dispatch_filters = {}
        self._gateway_url = ""
        self._log = logging.getLogger().getChild(type(self).__name__)
        self._sequence_index = None
        self._session_id = None
        self._settings = kwargs
        self._token = token
        self._observer: Optional[asyncio.Future] = None
        self._websocket = asyncio.Future()

        self.events.on(Event.READY, self._ready)
        self.events.raw.on(self._reconnect, op_code=GatewayCode.RECONNECT)

    @property
    def connected(self) -> bool:
        return self._connected.is_set()

    @property
    def gateway(self) -> str:
        return self._gateway_url

    @property
    def sequence_index(self) -> Optional[int]:
        return self._sequence_index

    async def connect(self):
        if not self.context.has(BaseHeartbeat):
            self.context.create(Heartbeat)

        self._log.info("Connecting to the Discord gateway")
        self.loop.create_task(self._connect())
        await self._connected.wait()
        self._log.info("Authenticating with gateway")
        await self._identify()

        while self._observer and not self._observer.done():
            await self._observer

    async def disconnect(self, code=1000):
        if self._connected:
            self._log.info(f"Disconnecting from the gateway with code {code}")
            self._connected.clear()
            ws: ClientWebSocketResponse = await self._websocket
            await ws.close(code=code)
            self._observer.cancel()

    async def resume(self):
        await self.disconnect(0)  # Close with a non-1000 code
        self._log.info("Reconnecting to gateway")
        self.loop.create_task(self._connect())
        await self._connected.wait()
        self._log.info("Attempting to resume session")
        self.loop.create_task(self._resume())
        event: Payload = await self.events.raw.next
        if event.op_code == GatewayCode.INVALID_SESSION:
            delay = random.uniform(1, 5)
            self._log.info(
                f"Failed to resume session, sleeping {delay:.2f}s then re-authenticating"
            )
            await asyncio.sleep(delay)
            await self._identify()
        self._log.info("Successfully reconnected")

    async def send(self, payload: Payload):
        ws = await self._websocket
        await ws.send_json(payload.dict(by_alias=True))

    async def _cache_gateway(self, session: ClientSession):
        response = await session.get(
            f"https://discord.com/api/v{self.__gateway_version__}/gateway"
        )
        try:
            data = json.loads(await response.read())
            self._gateway_url = data["url"]
        except (json.decoder.JSONDecodeError, KeyError):
            raise ValueError(
                f"API response was not as expected, gateway version {self.__gateway_version__} may be out of date"
            )

    async def _connect(self):
        if not self.gateway:
            await self._cache_gateway(self.api.session)

        try:
            ws = await self._create_websocket(self.api.session)
            self._websocket.set_result(ws)
            self._connected.set()
            self._observer = self.loop.create_task(self._observe(ws))
            await self._observer
        except client_exceptions.ClientConnectorError:
            raise ConnectionError(
                f"Gateway connection failed, attempted to connect to {self.gateway!r}, it may be out of date"
            )
        else:
            if ws and not ws.closed:
                await ws.close()
        finally:
            self._connected.clear()
            self._websocket = asyncio.Future()

    async def _create_websocket(
        self, session: ClientSession
    ) -> ClientWebSocketResponse:
        return await session.ws_connect(self.gateway)

    async def _emit_binary(self, data: bytes):
        decompressed_data = zlib.decompressobj().decompress(data).decode("utf-8")
        await self._emit_text(decompressed_data)

    async def _emit_text(self, data: str):
        payload = Payload(**json.loads(data))
        if payload.sequence_num and (
            not self.sequence_index or payload.sequence_num > self.sequence_index
        ):
            self._sequence_index = payload.sequence_num
        self.events.push(payload)

    def _identify(self):
        settings = self._settings.copy()
        data = {
            "token": self._token,
            "intents": settings.pop("intents", Intents.DEFAULT),
            "compress": settings.pop("compress", True),
            "properties": {
                "$os": sys.platform,
                "$browser": settings.pop("browser", "dippy.core"),
                "$device": settings.pop("device", "dippy.core"),
            },
        }
        data.update(settings)
        return self.send(Payload(op=GatewayCode.IDENTIFY, d=data))

    async def _observe(self, websocket: ClientWebSocketResponse):
        while self.connected:
            message = await websocket.receive()
            if message.type in {
                WSMsgType.CLOSE,
                WSMsgType.CLOSING,
                WSMsgType.CLOSED,
            }:
                self._log.error(f"Gateway connection closed - {message}")
                if self._connected.is_set():
                    self._connected.clear()
                    delay = random.uniform(2, 5)
                    self._log.info(
                        f"Attempting to resume after a {delay:.2f}s standoff"
                    )
                    await asyncio.sleep(delay)
                    self.loop.create_task(self.resume())
                    return
            elif message.type == WSMsgType.ERROR:
                self._log.error(f"The connection returned an error: {message.data}")
                raise message.data
            # Handle TEXT and BINARY messages. Kick them out to a task so that the observer loop can continue.
            elif message.type == WSMsgType.TEXT:
                self.loop.create_task(self._emit_text(message.data))
            elif message.type == WSMsgType.BINARY:
                self.loop.create_task(self._emit_binary(message.data))

    async def _ready(self, event: EventReady):
        self._session_id = event.session_id

    async def _reconnect(self, _):
        await self.resume()

    def _resume(self):
        return self.send(
            Payload(
                op=GatewayCode.RESUME,
                d={
                    "token": self._token,
                    "session_id": self._session_id,
                    "seq": self._sequence_index,
                },
            )
        )
