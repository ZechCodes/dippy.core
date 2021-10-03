from __future__ import annotations
from bevy.inject import Inject as _Inject, Injectable as _Injectable
from dippy.core.datetime_helpers import from_string, datetime
from functools import partial as _partial
from types import MappingProxyType as _MappingProxyType
import dataclasses as _d
import textwrap as _textwrap
import dippy.core.cache.manager as _cache
import typing as _t


NOTSET = type("NOTSET", (object,), {"__repr__": lambda s: "NOTSET"})()

_CONVERTER = _t.Callable[[_t.Any], _t.Any]
_VALIDATOR = _t.Callable[[_t.Any], bool]


_converters: dict[_t.Type, _CONVERTER] = {}
_validators: dict[_t.Type, _VALIDATOR] = {}


def safe_is_subclass(cls, base_type) -> bool:
    if not isinstance(cls, type):
        return False

    return issubclass(cls, base_type)


@_t.overload
def register_converter(type_: _t.Type) -> _t.Callable[[_CONVERTER], _CONVERTER]:
    ...


@_t.overload
def register_converter(type_: _t.Type, converter: _CONVERTER) -> _CONVERTER:
    ...


def register_converter(
    type_: _t.Type, converter: _t.Optional[_CONVERTER] = None
) -> _t.Union[_CONVERTER, _t.Callable[[_CONVERTER], _CONVERTER]]:
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
        return _partial(register_converter, type_)

    _converters[type_] = converter
    return converter


def find_converter(converter_type: _t.Type) -> _t.Optional[_CONVERTER]:
    """Finds a converter for the given type. This will return None if no convert is registered for the type."""
    for type_, converter in _converters.items():
        if issubclass(converter_type, type_):
            return converter


@_t.overload
def register_validator(type_: _t.Type) -> _t.Callable[[_CONVERTER], _VALIDATOR]:
    ...


@_t.overload
def register_validator(type_: _t.Type, validator: _VALIDATOR) -> _VALIDATOR:
    ...


def register_validator(
    type_: _t.Type, validator: _t.Optional[_VALIDATOR] = None
) -> _t.Union[_VALIDATOR, _t.Callable[[_VALIDATOR], _VALIDATOR]]:
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
        return _partial(register_validator, type_)

    _validators[type_] = validator
    return validator


def find_validator(validator_type: _t.Type) -> _t.Optional[_VALIDATOR]:
    """Finds a validator for the given type. This will return None if no validator is registered for the type."""
    for type_, validator in _validators.items():
        if issubclass(validator_type, type_):
            return validator


register_converter(datetime, lambda v: from_string(v) if isinstance(v, str) else v)


@_d.dataclass
class Field:
    default: _t.Any = NOTSET
    index: bool = False
    key_name: _t.Optional[str] = None
    assignable: bool = False
    converters: _t.Iterable[_CONVERTER] = _d.field(default_factory=tuple)
    validators: _t.Iterable[_VALIDATOR] = _d.field(default_factory=tuple)
    annotation: _t.Optional[_t.Any] = _d.field(default=None, init=False)

    @property
    def model_type(self) -> _t.Optional[Model]:
        annotation = _t.get_origin(self.annotation) or self.annotation
        if safe_is_subclass(annotation, Model):
            return annotation

        args = _t.get_args(self.annotation)
        if args:
            annotation = _t.get_origin(args[0]) or args[0]
            if safe_is_subclass(annotation, _t.Iterable):
                args = _t.get_args(args[0])
                annotation = _t.get_origin(args[0]) or args[0]

            if safe_is_subclass(annotation, Model):
                return annotation

        return None

    @property
    def container_type(self) -> _t.Optional[_t.Type]:
        annotation = _t.get_origin(self.annotation) or self.annotation
        if annotation is _t.Union:
            args = _t.get_args(annotation)
            annotation = _t.get_origin(args[0]) or args[0]

        if safe_is_subclass(annotation, _t.Iterable):
            return _t.get_origin(annotation) or annotation

        return None

    @property
    def is_optional(self) -> bool:
        if _t.get_origin(self.annotation) is not _t.Union:
            return False

        return type(None) in _t.get_args(self.annotation)

    def add_type_converter(self, converter: _CONVERTER):
        self.converters = (converter, *self.converters)

    def add_type_validator(self, validator: _VALIDATOR):
        self.validators = (validator, *self.validators)


class Model(_Injectable):
    """Base class for constructing models in a declarative fashion that rely on an underlying state dictionary. The
    intention is to allow for objects that can share cached state.

    Example:
    ```python
    class ExampleModel(Model):
        id: Snowflake = Field(index=True)
        name: str
        roles: list[Role]
    ```
    The fields are built using the init subclass hook, so it is necessary to inherit from the model base class or one of
    its subclasses.

    It is possible to save a models state by taking a snapshot which will return a model of the same type with a deep
    copy of the underlying state dictionary.

    The underlying state is accessible through the __dippy_state__ property."""

    __slots__ = ["_state", "_snapshot"]
    cache: _Inject[_cache.CacheManager]
    __dippy_index_fields__: tuple[str, ...] = tuple()
    __dippy_cache_type__: _t.Optional[str] = None

    def __init_subclass__(cls, cache_type: _t.Optional[str] = None, **kwargs):
        cls.cache = _Inject(_cache.CacheManager)
        cls._build_fields()
        cls._set_cache_type(cache_type)

    def __init__(self, state: dict[str, _t.Any], *, snapshot: bool = False):
        self._snapshot = snapshot
        self._state = state

    @property
    def __dippy_index__(self) -> tuple[_t.Any]:
        """A tuple containing the values that should be used to identify the instance. Useful for caching."""
        return tuple(getattr(self, name) for name in self.__dippy_index_fields__)

    @property
    def __dippy_state__(self) -> _MappingProxyType:
        """Immutable view of the model's state mapping."""
        return _MappingProxyType(self._state)

    def is_snapshot(self) -> bool:
        """Is the dictionary a snapshot of an existing model."""
        return self._snapshot

    def snapshot(self) -> Model:
        """Create a model instance that is bound to a copy of the current model's state."""
        if self.is_snapshot():
            return self

        return type(self)(self._state.copy(), snapshot=True)

    def _get_model_container(
        self,
        value: _cache.DiscordObject,
        container: _t.Type[_t.Sequence],
        model: _t.Type[ModelType],
    ) -> _t.Sequence[ModelType]:
        return container(self._get_model(item, model) for item in value)

    def _get_model(
        self, value: _cache.DiscordObject, model: _t.Type[ModelType]
    ) -> _t.Optional[ModelType]:
        if model.__dippy_cache_type__:
            return self._get_model_from_cache(value, model)
        return self.__bevy_context__.build(model, value)

    def _get_model_from_cache(
        self, value: _cache.DiscordObject, model: _t.Type[ModelType]
    ) -> _t.Optional[ModelType]:
        key = self.cache.get_key(model, value)
        ret = self.cache.get(model, *key)
        if not ret:
            self.cache.update(model, value, *key)
            ret = self.cache.get(model, *key)
        return ret

    @classmethod
    def _build_fields(cls):
        fields = list(cls._get_fields())
        cls._create_properties(fields)
        cls._save_index_fields(fields)

    @classmethod
    def _configure_field_annotation(cls, field: Field, annotation: _t.Any):
        types = cls._get_annotation_types(annotation)
        field.add_type_validator(cls._create_validator(types))
        field.add_type_converter(cls._create_converter(types))

    @staticmethod
    def _create_converter(types: tuple[_t.Type]) -> _CONVERTER:
        converters = [find_converter(type_) for type_ in types]

        def converter(value: _t.Any) -> _t.Any:
            if value is NOTSET and type(None) in types:
                return

            for converter_ in converters:
                if converter_:
                    value = converter_(value)

            return value

        return converter

    @classmethod
    def _create_properties(cls, fields: _t.Iterable[tuple[str, Field]]):
        for name, field in fields:
            property_ = cls._create_property_method(name, field)
            setattr(cls, name, property_)

    @staticmethod
    def _create_property_method(name: str, field: Field) -> property:
        method = _textwrap.dedent(
            f"""
            @property
            def {name}(self):
                value = self._state.get("{name}", NOTSET)
                if field.default is not NOTSET and value is NOTSET:
                    return field.default

                for converter in field.converters:
                    value = converter(value)
                    
                if field.model_type:
                    if field.container_type:
                        value = self._get_model_container(value, field.container_type, field.model_type)
                    else:
                        value = self._get_model(value, field.model_type)

                return value"""
        )

        if field.assignable:
            method += _textwrap.dedent(
                f"""
                @{name}.setter
                def {name}(self, value):
                    for converter in field.converters:
                        value = converter(value)
        
                    for validator in field.validators:
                        if not validator(value):
                            return            
        
                    self._state["{name}"] = value
                """
            )

        exec(method, {"field": field, **globals()}, locals_ := {})
        return _t.cast(property, locals_[name])

    @staticmethod
    def _create_validator(types: tuple[_t.Type]) -> _VALIDATOR:
        def validator(value: _t.Any) -> bool:
            if value is None and type(None) in types:
                return True

            validator_ = find_validator(type(value))
            if validator_ and not validator_(value):
                return False

            for type_ in types:
                try:
                    if isinstance(value, type_):
                        return True
                except TypeError:
                    pass

            else:
                return False

        return validator

    @staticmethod
    def _get_annotation_types(annotation: _t.Any) -> tuple[_t.Type]:
        types = (_t.cast(_t.Type, annotation),)
        if _t.get_origin(annotation) is _t.Union:
            types = _t.get_args(annotation)
        return types

    @classmethod
    def _get_fields(cls) -> _t.Generator[tuple[str, Field], None, None]:
        for name, annotation in _t.get_type_hints(cls).items():
            field = getattr(cls, name, NOTSET)
            if field is NOTSET and not isinstance(annotation, _Inject):
                field = Field(key_name=name)

            if isinstance(field, Field):
                field.annotation = annotation
                if not field.key_name:
                    field.key_name = name

                cls._configure_field_annotation(field, annotation)
                yield name, field

    @classmethod
    def _save_index_fields(cls, fields: _t.Iterable[tuple[str, Field]]):
        cls.__dippy_index_fields__ = (
            *cls.__dippy_index_fields__,
            *(name for name, field in fields if field.index),
        )

    @classmethod
    def _set_cache_type(cls, cache_type: _t.Optional[str]):
        if cache_type:
            cls.__dippy_cache_type__ = cache_type


ModelType = _t.TypeVar("ModelType", bound=Model)