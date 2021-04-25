from bevy import Injectable
from datetime import datetime, timedelta
from dippy.core.enums import GatewayCode
from dippy.core.events import BaseEventStream
from dippy.core.gateway.bases import BaseGatewayConnection, BaseHeartbeat
from dippy.core.gateway.payload import Payload
from typing import Awaitable, Optional
import asyncio
import logging
import random
import time


class Heartbeat(BaseHeartbeat, Injectable):
    events: BaseEventStream
    gateway: BaseGatewayConnection
    loop: asyncio.AbstractEventLoop

    def __init__(self):
        self._interval = -1
        self._log = logging.getLogger().getChild(type(self).__name__)
        self._next_beat: Optional[asyncio.Future] = None
        self._last_acknowledgement = time.time()

        # Immediate heartbeat requested
        self.events.raw.on(self._send_immediately, op_code=GatewayCode.HEARTBEAT)
        # Heartbeat interval settings
        self.events.raw.on(self._start, op_code=GatewayCode.HELLO)
        # Heartbeat acknowledgement
        self.events.raw.on(
            self._note_acknowledgement, op_code=GatewayCode.HEARTBEAT_ACK
        )

    @property
    def running(self) -> bool:
        return self._next_beat is not None and not self._next_beat.done()

    def stop(self):
        self._next_beat.cancel()
        self._next_beat = None

    def _note_acknowledgement(self, payload: Payload):
        self._last_acknowledgement = time.time()

    def _schedule_first_heartbeat(self):
        delay_ms = random.random() * self._interval
        next_beat = datetime.utcnow() + timedelta(milliseconds=delay_ms)
        self._log.debug(
            f"Scheduling first heartbeat to be sent in {delay_ms/1000:.2f}s at {next_beat.isoformat(' ')} UTC"
        )
        self._schedule_next_heartbeat(delay_ms)

    def _schedule_next_heartbeat(self, delay_ms: float):
        self._next_beat = self.loop.create_task(self._send_heartbeat(delay_ms))

    async def _send_heartbeat(self, delay_ms: float):
        if delay_ms:
            await self._sleep(delay_ms)
            if time.time() - self._last_acknowledgement > self._interval:
                self._log.info("No heartbeat acknowledgement has been received")
                await self.gateway.resume()
                return

        if self.gateway.connected:
            await self.gateway.send(
                Payload(op=GatewayCode.HEARTBEAT, d=self.gateway.sequence_index)
            )
            next_beat = datetime.utcnow() + timedelta(milliseconds=self._interval)
            self._log.debug(
                f"Scheduling next heartbeat to be sent at {next_beat.isoformat(' ')} UTC"
            )
            self._schedule_next_heartbeat(self._interval)

    def _send_immediately(self, payload: Payload):
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
