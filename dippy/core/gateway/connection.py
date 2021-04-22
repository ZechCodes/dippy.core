from aiohttp import client_exceptions, ClientSession, ClientWebSocketResponse, WSMsgType
from dippy.core.gateway.payload import Payload
from dippy.core.gateway.heartbeat import Heartbeat
from dippy.core.intents import Intents
from gully import Gully, Observer
from typing import Callable, Coroutine, Optional, Union
import asyncio
import json
import logging
import random
import sys
import zlib


class GatewayConnection:
    __gateway_version__ = 8

    def __init__(self, token: str, *, loop: asyncio.AbstractEventLoop = None, **kwargs):
        self._client_events = Gully()
        self._connected = asyncio.Event()
        self._filters = {}
        self._gateway_url = ""
        self._heartbeat = Heartbeat(self, loop=loop)
        self._log = logging.getLogger().getChild(type(self).__name__)
        self._loop = loop if loop else asyncio.get_event_loop()
        self._sequence_index = None
        self._session_id = None
        self._settings = kwargs
        self._token = token
        self._observer: Optional[asyncio.Future] = None
        self._websocket = asyncio.Future()

        self.on(self._ready, event="READY")

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
        self._log.info("Connecting to the Discord gateway")
        self._loop.create_task(self._connect())
        await self._connected.wait()
        self._log.info("Authenticating with gateway")
        await self._identify()

    async def disconnect(self, code=1000):
        if self._connected:
            self._log.info(f"Disconnecting from the gateway with code {code}")
            ws: ClientWebSocketResponse = await self._websocket
            await ws.close(code=code)
            self._observer.cancel()

    def on(
        self,
        callback: Union[Callable, Coroutine],
        op_code: Optional[int] = None,
        event: Optional[str] = None,
    ) -> Observer:
        if (op_code, event) not in self._filters:
            self._filters[(op_code, event)] = self._client_events.filter(
                lambda payload: (op_code is None or op_code == payload.op_code)
                and (event is None or event == payload.event)
            )

        return self._filters[(op_code, event)].watch(callback)

    async def resume(self):
        await self.disconnect(0)  # Close with a non-1000 code
        self._log.info("Reconnecting to gateway")
        self._loop.create_task(self._connect())
        await self._connected.wait()
        self._log.info("Attempting to resume session")
        self._loop.create_task(self._resume())
        event: Payload = await self._client_events.next
        if event.op_code == 9:
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
        async with ClientSession() as session:
            if not self.gateway:
                await self._cache_gateway(session)

            try:
                ws = await self._create_websocket(session)
                self._websocket.set_result(ws)
                self._connected.set()
                self._observer = self._loop.create_task(self._observe(ws))
                await self._observer
            except client_exceptions.ClientConnectorError:
                raise ConnectionError(
                    f"Gateway connection failed, attempted to connect to {self.gateway!r}, it may be out of date"
                )
            finally:
                self._connected.clear()
                if ws and not ws.closed:
                    await ws.close()
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
        self._client_events.push(payload)

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
        return self.send(Payload(op=2, d=data))

    async def _observe(self, websocket: ClientWebSocketResponse):
        while self.connected:
            message = await websocket.receive()
            if message.type in {
                WSMsgType.CLOSE,
                WSMsgType.CLOSING,
                WSMsgType.CLOSED,
            }:
                raise ConnectionError(
                    f"Gateway connection closed unexpectedly - {message}"
                )
            elif message.type == WSMsgType.ERROR:
                self._log.error(f"The connection returned an error: {message.data}")
                raise message.data
            # Handle TEXT and BINARY messages. Kick them out to a task so that the observer loop can continue.
            elif message.type == WSMsgType.TEXT:
                self._loop.create_task(self._emit_text(message.data))
            elif message.type == WSMsgType.BINARY:
                self._loop.create_task(self._emit_binary(message.data))

    async def _ready(self, payload: Payload):
        self._session_id = payload.data["session_id"]

    def _resume(self):
        return self.send(
            Payload(
                op=6,
                d={
                    "token": self._token,
                    "session_id": self._session_id,
                    "seq": self._sequence_index,
                },
            )
        )
