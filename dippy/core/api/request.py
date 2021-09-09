from __future__ import annotations
from attr import attrs, attrib, Attribute, resolve_types
from dippy.core.not_set import NOT_SET
from dippy.core.converters import build_converter
from typing import Any, Callable, Optional, Protocol, TypeVar


_ConverterType = TypeVar("_ConverterType")
_ValidatorArgType = TypeVar("_ValidatorArgType")
_T = TypeVar("_T")


def setup_converters(cls, fields: list[Attribute]) -> list[Attribute]:
    resolve_types(cls, attribs=fields)
    return [a.evolve(converter=build_converter(a)) for a in fields]


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
