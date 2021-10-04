from functools import partial
import typing


CONVERTER = typing.Callable[[typing.Any], typing.Any]
_converters: dict[typing.Type, CONVERTER] = {}


@typing.overload
def register_converter(type_: typing.Type) -> typing.Callable[[CONVERTER], CONVERTER]:
    ...


@typing.overload
def register_converter(type_: typing.Type, converter: CONVERTER) -> CONVERTER:
    ...


def register_converter(
    type_: typing.Type, converter: typing.Optional[CONVERTER] = None
) -> typing.Union[CONVERTER, typing.Callable[[CONVERTER], CONVERTER]]:
    """Registers a function as a converter for the given type. This can either be used directly as a function that takes
    a type and a function, or it can be used as a decorator by passing it just a type.
    ```python
    register_converter(dict, dict_converter)
    ```
    Or as a decorator
    ```python
    @register_converter(dict)
    def dict_converter(value: Any) -> dict[str, Any]:
        ...
    ```"""
    if not converter:
        return partial(register_converter, type_)

    _converters[type_] = converter
    return converter


def find_converter(converter_type: typing.Type) -> typing.Optional[CONVERTER]:
    """Finds a converter for the given type. This will return None if no convert is registered for the type."""
    for type_, converter in _converters.items():
        if issubclass(converter_type, type_):
            return converter
