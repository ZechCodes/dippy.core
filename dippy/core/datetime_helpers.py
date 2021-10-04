"""Simple datetime helper module to ensure that all datetimes are UTC localized."""
from dippy.core.model.converters import register_converter
from typing import Union
import pendulum


datetime = pendulum.DateTime  # Just for convenience so we only need one import


def now() -> pendulum.datetime:
    """Gets a datetime for the current time, that is localized to UTC."""
    return pendulum.now(pendulum.UTC)


@register_converter(datetime)
def from_string(iso8601_datetime_string: str) -> pendulum.datetime:
    """Converts a datetime string to a datetime that is localized to UTC."""
    if not isinstance(iso8601_datetime_string, str):
        return iso8601_datetime_string

    return pendulum.parse(iso8601_datetime_string, tz=pendulum.UTC)


def from_timestamp(timestamp: Union[int, float]) -> pendulum.datetime:
    """Converts a timestamp to a datetime that is localized to UTC."""
    return pendulum.from_timestamp(timestamp, pendulum.UTC)
