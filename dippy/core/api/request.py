from __future__ import annotations
from attr import attrs, attrib, converters, validators
from dippy.core.models.base_model import BaseModel
from typing import Callable, Optional, Protocol, TypeVar


NOT_SET = type("NOT_SET", (object,), {"__repr__": lambda s: "NOT_SET"})
_ConverterType = TypeVar("_ConverterType")
_ValidatorArgType = TypeVar("_ValidatorArgType")
_T = TypeVar("_T")


def model(func):
    return attrs(auto_attribs=True)(func)


@model
class BaseRequest(Protocol):
    endpoint: str
    method: str
    model: Optional[BaseModel]


def query_arg(
    default: Optional[_T] = NOT_SET,
    validator: Optional[_ValidatorArgType[_T]] = None,
    converter: Optional[_ConverterType] = None,
    factory: Optional[Callable[[], _T]] = None,
):
    kwargs = {"metadata": {"query_arg": True}, "kw_only": True, "default": default}

    if validator:
        kwargs["validator"] = validator

    if converter:
        kwargs["converter"] = converter

    if factory:
        kwargs["factory"] = factory

    return attrib(**kwargs)


def url_arg(
    default: Optional[_T] = NOT_SET,
    validator: Optional[_ValidatorArgType[_T]] = None,
    converter: Optional[_ConverterType] = None,
    factory: Optional[Callable[[], _T]] = None,
):
    kwargs = {"metadata": {"query_arg": False}}
    if default is not NOT_SET:
        kwargs["default"] = default

    if validator:
        kwargs["validator"] = validator

    if converter:
        kwargs["converter"] = converter

    if factory:
        kwargs["factory"] = factory

    return attrib(**kwargs)
