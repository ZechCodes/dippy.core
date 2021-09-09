from attr import converters
from dippy.core.not_set import NOT_SET
from dippy.core.enums.enums import Enum
from typing import get_args, get_origin, Union


def build_converter(attribute):
    converter = attribute.converter
    if not attribute.converter:
        converter = attribute.type
        if get_origin(converter) is Union:
            args = get_args(converter)
            converter = args[0]
            if isinstance(converter, Enum):
                converter = converter.safe_get
            if None in args:
                converter = converters.default_if_none(converter)

    return lambda value: value if value is NOT_SET else converter(value)
