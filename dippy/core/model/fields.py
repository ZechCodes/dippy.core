from __future__ import annotations
from dataclasses import dataclass, field as dataclass_field
from dippy.core.cache.manager import CacheManager, DiscordObject
from dippy.core.enums.enums import Enum
from dippy.core.model.annotions import AnnotationWrapperGetter
from dippy.core.model.converters import find_converter, CONVERTER
from dippy.core.model.validators import find_validator, VALIDATOR
import bevy
import dippy.core.model.models as models
import typing


NOTSET = type("NOTSET", (object,), {"__repr__": lambda s: "NOTSET"})()


def safe_is_subclass(cls, base_type) -> bool:
    if not isinstance(cls, type):
        return False

    return issubclass(cls, base_type)


@dataclass
class Field:
    default: typing.Any = NOTSET
    index: bool = False
    key_name: typing.Optional[str] = None
    assignable: bool = False
    converter: typing.Optional[CONVERTER] = None
    validator: typing.Optional[VALIDATOR] = None
    raw_annotation: AnnotationWrapperGetter = dataclass_field(init=False)

    def __get__(self, model: typing.Optional[models.Model], cls: typing.Type[models.Model]) -> typing.Any:
        if not model:
            return self

        value = model.__dippy_state__.get(self.key_name, NOTSET)
        if value is NOTSET:
            return None if self.default is NOTSET else self.default

        value = self._apply_converters(value)
        if self.model_type:
            if self.container_type:
                value = self._build_model_container(value, model.__bevy_context__, model.cache)
            else:
                value = self._build_model(value, model.__bevy_context__, model.cache)

        return value

    def __set__(self, model: models.Model, value: typing.Any):
        if not self.assignable:
            raise AttributeError(f"The {type(model).__qualname__}.{self.key_name} field is not assignable")

        if not self._validate(value):
            return

        model.__dippy_state__[self.key_name] = self._apply_converters(value)

    @property
    def annotation(self) -> typing.Any:
        return self.raw_annotation.get()

    @property
    def model_type(self) -> typing.Optional[typing.Type[models.Model]]:
        """Parses the models type from the annotation. This will look at the first arg of union and container types when
        present. If no models type is found it will return None."""
        raw_annotation = self.annotation
        annotation = typing.get_origin(raw_annotation) or raw_annotation
        if safe_is_subclass(annotation, models.Model):
            return annotation

        args = typing.get_args(raw_annotation)
        if args:
            annotation = typing.get_origin(args[0]) or args[0]
            if safe_is_subclass(annotation, typing.Sequence) and not safe_is_subclass(annotation, str):
                args = typing.get_args(args[0])
                annotation = typing.get_origin(args[0]) or args[0]

            if safe_is_subclass(annotation, models.Model):
                return annotation

        return None

    @property
    def container_type(self) -> typing.Optional[typing.Type]:
        """Parses the container type from the annotation. If no container type is found it will return None."""
        annotation = typing.get_origin(self.annotation) or self.annotation
        if annotation is typing.Union:
            args = typing.get_args(annotation)
            annotation = typing.get_origin(args[0]) or args[0]

        if safe_is_subclass(annotation, typing.Iterable):
            return typing.get_origin(annotation) or annotation

        return None

    @property
    def is_optional(self) -> bool:
        """Checks for a union type that includes a none type."""
        if typing.get_origin(self.annotation) is not typing.Union:
            return False

        return type(None) in typing.get_args(self.annotation)

    def _apply_converters(self, value: typing.Any) -> typing.Any:
        value = self._apply_type_converter(value)
        if self.converter:
            value = self.converter(value)
        value = self._build_enum_type(value)
        return value

    def _apply_type_converter(self, value: typing.Any) -> typing.Any:
        types = self._get_annotation_types()
        converters = (c for type_ in types if (c := find_converter(type_)))
        for converter in converters:
            value = converter(value)

        return value

    def _build_enum_type(self, value: typing.Any) -> typing.Any:
        raw_annotation = self.annotation
        annotation = typing.get_origin(raw_annotation) or raw_annotation
        if isinstance(annotation, type) and isinstance(value, str):
            args = typing.get_args(raw_annotation)
            if args:
                annotation = typing.get_origin(args[0]) or args[0]

            if isinstance(annotation, type) and issubclass(annotation, Enum):
                return annotation.safe_get(value)

        return value

    def _build_model(self, value: DiscordObject, context: bevy.Context, cache: CacheManager) -> typing.Optional[Model]:
        if self.model_type.__dippy_cache_type__:
            return self._get_model_from_cache(value, cache)
        return context.build(self.model_type, value)

    def _build_model_container(
        self, value: typing.Sequence[DiscordObject], context: bevy.Context, cache: CacheManager
    ) -> typing.Sequence[models.Model]:
        return self.container_type(self._build_model(item, context, cache) for item in value)

    def _get_annotation_types(self) -> tuple[typing.Type, ...]:
        annotation = self.annotation
        types = (typing.cast(typing.Type, annotation),)
        if typing.get_origin(annotation) is typing.Union:
            types = typing.get_args(annotation)

        return tuple(typing.cast(typing.Type, typing.get_origin(t) or t) for t in types)

    def _get_model_from_cache(self, value: DiscordObject, cache: CacheManager) -> typing.Optional[models.Model]:
        model = self.model_type
        if not model:
            return

        key = cache.get_key(model, value)
        ret = cache.get(model, *key)
        if not ret:
            cache.update(model, value, *key)
            ret = cache.get(model, *key)

        return ret

    def _validate(self, value: typing.Any) -> bool:
        if value is None and self.is_optional:
            return True

        if self._run_type_validators(value):
            return True

        validator = find_validator(type(value))
        return validator and validator(value)

    def _run_type_validators(self, value: typing.Any) -> bool:
        types = self._get_annotation_types()
        for type_ in types:
            try:
                if isinstance(value, type_):
                    return True
            except TypeError:
                pass

        else:
            return False


class JSONField(Field):
    ...


class QueryArgField(Field):
    ...
