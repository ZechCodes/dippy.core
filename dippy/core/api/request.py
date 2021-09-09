from __future__ import annotations
from attr import attrs, attrib, Attribute, converters, validators, resolve_types
from dippy.core.models.base_model import BaseModel
from dippy.core.enums.enums import Enum
from typing import (
    Any,
    Callable,
    Optional,
    Protocol,
    TypeVar,
    Union,
    get_args,
    get_origin,
)


NOT_SET = type("NOT_SET", (object,), {"__repr__": lambda s: "NOT_SET"})
_ConverterType = TypeVar("_ConverterType")
_ValidatorArgType = TypeVar("_ValidatorArgType")
_T = TypeVar("_T")


def setup_converters(cls, fields: list[Attribute]) -> list[Attribute]:
    resolve_types(cls, attribs=fields)
    return [a.evolve(converter=_build_converter(a)) for a in fields]


def _build_converter(attribute):
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


def request_model(func):
    return attrs(field_transformer=setup_converters)(func)


@request_model
class BaseRequest(Protocol):
    endpoint: str
    method: str


def json_arg(
    default: Optional[_T] = NOT_SET,
    validator: Optional[_ValidatorArgType[_T]] = None,
    converter: Optional[_ConverterType] = None,
    factory: Optional[Callable[[], _T]] = None,
):
    kwargs = _build_kwargs(validator, converter, factory)
    kwargs["metadata"] = {"arg_type": "json"}
    kwargs["kw_only"] = True
    kwargs["default"] = default

    return attrib(**kwargs)


def query_arg(
    default: Optional[_T] = NOT_SET,
    validator: Optional[_ValidatorArgType[_T]] = None,
    converter: Optional[_ConverterType] = None,
    factory: Optional[Callable[[], _T]] = None,
):
    kwargs = _build_kwargs(validator, converter, factory)
    kwargs["metadata"] = {"arg_type": "query"}
    kwargs["kw_only"] = True
    kwargs["default"] = default

    return attrib(**kwargs)


def url_arg(
    default: Optional[_T] = NOT_SET,
    validator: Optional[_ValidatorArgType[_T]] = None,
    converter: Optional[_ConverterType] = None,
    factory: Optional[Callable[[], _T]] = None,
):
    kwargs = _build_kwargs(validator, converter, factory)
    kwargs["metadata"] = {"arg_type": "url"}
    if default is not NOT_SET:
        kwargs["default"] = default

    return attrib(**kwargs)


def _build_kwargs(validator, converter, factory) -> dict[str, Any]:
    kwargs = {}
    if validator:
        kwargs["validator"] = validator

    if converter:
        kwargs["converter"] = converter

    if factory:
        kwargs["factory"] = factory

    return kwargs
