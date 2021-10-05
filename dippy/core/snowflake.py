from __future__ import annotations
from dippy.core.datetime_helpers import datetime, from_timestamp
from dippy.core.model.converters import register_converter
from functools import cached_property
from typing import Union


class Snowflake:
    """Simple class for parsing Discord snowflakes.

    Provides instance properties for accessing the snowflake's increment, process ID, worker ID, and timestamp."""

    __discord_epoch_offset_ms = 1420070400000

    def __init__(self, snowflake: int):
        self._snowflake = int(snowflake)

    @cached_property
    def increment(self) -> int:
        return self._snowflake & self.__mask(12)

    @cached_property
    def process_id(self) -> int:
        return self._snowflake >> 12 & self.__mask(5)

    @cached_property
    def worker_id(self) -> int:
        return self._snowflake >> 17 & self.__mask(5)

    @cached_property
    def timestamp(self) -> datetime:
        return from_timestamp(
            ((self._snowflake >> 22) + self.__discord_epoch_offset_ms) / 1000
        )

    def __eq__(self, other):
        return isinstance(other, Snowflake) and hash(other) == hash(self)

    def __int__(self):
        return self._snowflake

    def __hash__(self):
        return self._snowflake

    def __str__(self):
        return str(self._snowflake)

    def __repr__(self):
        return f"{type(self).__name__}({self})"

    def __mask(self, size: int) -> int:
        return 2 ** size - 1


@register_converter(Snowflake)
def snowflake_converter(value: Union[str, int, Snowflake]):
    if isinstance(value, str):
        return Snowflake(int(value))

    if isinstance(value, int):
        return Snowflake(value)

    return value
