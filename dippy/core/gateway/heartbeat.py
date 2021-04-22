from dippy.core.gateway.payload import Payload
from typing import Awaitable, Optional
import asyncio
import logging
import random
import time


class Heartbeat:
    def __init__(
        self,
        gateway,
        *,
        loop: asyncio.AbstractEventLoop = None,
    ):
        self._gateway = gateway
        self._interval = -1
        self._log = logging.getLogger().getChild(type(self).__name__)
        self._loop = loop if loop else asyncio.get_event_loop()
        self._next_beat: Optional[asyncio.Future] = None
        self._last_acknowledgement = time.time()

        # Immediate heartbeat requested
        self._gateway.on(self._send_immediately, op_code=1)
        # Heartbeat interval settings
        self._gateway.on(self._start, op_code=10)
        # Heartbeat acknowledgement
        self._gateway.on(self._note_acknowledgement, op_code=11)

    @property
    def running(self) -> bool:
        return self._next_beat is not None

    def stop(self):
        self._next_beat.cancel()
        self._next_beat = None

    def _note_acknowledgement(self, payload: Payload):
        self._last_acknowledgement = time.time()

    def _schedule_first_heartbeat(self):
        delay_ms = random.random() * self._interval
        self._log.debug(
            f"Scheduling first heartbeat to be sent in {delay_ms / 1000:0.2f}s"
        )
        self._schedule_next_heartbeat(delay_ms)

    def _schedule_next_heartbeat(self, delay_ms: float):
        self._next_beat = self._loop.create_task(self._send_heartbeat(delay_ms))

    async def _send_heartbeat(self, delay_ms: float):
        if delay_ms:
            await self._sleep(delay_ms)
            if time.time() - self._last_acknowledgement > self._interval:
                self._log.info("No heartbeat acknowledgement has been received")
                await self._gateway.resume()
                return

        if self._gateway.connected:
            await self._gateway.send(Payload(op=1, d=self._gateway.sequence_index))
            self._log.debug(
                f"Scheduling next heartbeat to be sent in {self._interval / 1000}s"
            )
            self._schedule_next_heartbeat(self._interval)

    async def _send_immediately(self, payload: Payload):
        self.stop()
        self._schedule_next_heartbeat(0)

    def _sleep(self, delay_ms: float) -> Awaitable:
        return asyncio.sleep(delay_ms / 1000)

    async def _start(self, payload: Payload):
        self._log.debug("Starting heart beat")
        if self._next_beat:
            self.stop()

        self._interval = payload.data["heartbeat_interval"]
        self._log.debug(f"Heartbeat interval is {self._interval}")
        self._schedule_first_heartbeat()
