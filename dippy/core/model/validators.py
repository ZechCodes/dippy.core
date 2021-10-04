from functools import partial
import typing


VALIDATOR = typing.Callable[[typing.Any], bool]
_validators: dict[typing.Type, VALIDATOR] = {}


@typing.overload
def register_validator(type_: typing.Type) -> typing.Callable[[VALIDATOR], VALIDATOR]:
    ...


@typing.overload
def register_validator(type_: typing.Type, validator: VALIDATOR) -> VALIDATOR:
    ...


def register_validator(
    type_: typing.Type, validator: typing.Optional[VALIDATOR] = None
) -> typing.Union[VALIDATOR, typing.Callable[[VALIDATOR], VALIDATOR]]:
    """Registers a function as a validator for the given type. This can either be used directly as a function that takes
    a type and a function, or it can be used as a decorator by passing it just a type.
    ```python
    register_validator(dict, dict_validator)
    ```
    Or as a decorator
    ```python
    @register_converter(dict)
    def dict_validator(value: Any) -> bool:
        ...
    ```"""
    if not validator:
        return partial(register_validator, type_)

    _validators[type_] = validator
    return validator


def find_validator(validator_type: typing.Type) -> typing.Optional[VALIDATOR]:
    """Finds a validator for the given type. This will return None if no validator is registered for the type."""
    for type_, validator in _validators.items():
        if issubclass(validator_type, type_):
            return validator
