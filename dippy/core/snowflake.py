from __future__ import annotations
from dippy.core.datetime_helpers import datetime, from_timestamp
from functools import cached_property


class Snowflake(int):
    """Simple class for parsing Discord snowflakes. Inherit from int since a snowflake is just an int with special
    properties. Overrides dunder eq to enforce matching only snowflakes.

    Provides instance properties for accessing the snowflake's increment, process ID, worker ID, and timestamp."""

    __discord_epoch_offset_ms = 1420070400000

    @cached_property
    def increment(self) -> int:
        return self & self.__mask(12)

    @cached_property
    def process_id(self) -> int:
        return self >> 12 & self.__mask(5)

    @cached_property
    def worker_id(self) -> int:
        return self >> 17 & self.__mask(5)

    @cached_property
    def timestamp(self) -> datetime:
        return from_timestamp(((self >> 22) + self.__discord_epoch_offset_ms) / 1000)

    def __mask(self, size: int) -> int:
        return 2 ** size - 1
