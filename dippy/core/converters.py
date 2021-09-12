from attr import converters
from dippy.core.not_set import NOT_SET
from dippy.core.enums.enums import Enum
from typing import get_args, get_origin, Union


def build_converter(attribute):
    converter = attribute.converter
    if not attribute.converter:
        converter = attribute.type

    converter, optional = get_annotation_type(converter)

    if isinstance(converter, Enum):
        converter = converter.safe_get
    if optional:
        converter = converters.default_if_none(converter)

    return lambda value: value if value is NOT_SET else converter(value)


def get_annotation_type(annotation):
    optional = False
    while get_origin(annotation) is Union:
        args = get_args(annotation)
        annotation = args[0]
        optional = optional or None in args

    return annotation, optional
