from __future__ import annotations as _
from dippy.core.cache.manager import CacheManager, DiscordObject
from dippy.core.model.annotions import AnnotationWrapper
import bevy.inject as bevy
import dippy.core.model.fields as fields
import typing


class Model(bevy.Injectable):
    """Base class for constructing models in a declarative fashion that rely on an underlying state dictionary. The
    intention is to allow for objects that can share cached state.

    Example:
    ```python
    class ExampleModel(Model):
        id: Snowflake = Field(index=True)
        name: str
        roles: list[Role]
    ```
    The fields are built using the init subclass hook, so it is necessary to inherit from the models base class or one of
    its subclasses.

    It is possible to save a models state by taking a snapshot which will return a models of the same type with a deep
    copy of the underlying state dictionary.

    The underlying state is accessible through the __dippy_state__ property."""

    __slots__ = ["_state", "_snapshot"]
    cache: bevy.Inject[CacheManager]
    __dippy_index_fields__: tuple[str, ...] = tuple()
    __dippy_cache_type__: typing.Optional[str] = None

    def __init_subclass__(cls, cache_type: typing.Optional[str] = None, **kwargs):
        cls.cache = bevy.Inject(CacheManager)
        cls._build_fields()
        cls._set_cache_type(cache_type)

    def __init__(self, state: dict[str, typing.Any], *, snapshot: bool = False):
        self._snapshot = snapshot
        self._state = state

    @property
    def __dippy_index__(self) -> tuple[typing.Any]:
        """A tuple containing the values that should be used to identify the instance. Useful for caching."""
        return tuple(getattr(self, name) for name in self.__dippy_index_fields__)

    @property
    def __dippy_state__(self) -> dict[str, typing.Any]:
        return self._state

    def is_snapshot(self) -> bool:
        """Is the dictionary a snapshot of an existing models."""
        return self._snapshot

    def snapshot(self) -> Model:
        """Create a models instance that is bound to a copy of the current models's state."""
        if self.is_snapshot():
            return self

        return type(self)(self._state.copy(), snapshot=True)

    def _get_model_container(
        self,
        value: DiscordObject,
        container: typing.Type[typing.Sequence],
        model: typing.Type[ModelType],
    ) -> typing.Sequence[ModelType]:
        return container(self._get_model(item, model) for item in value)

    def _get_model(self, value: DiscordObject, model: typing.Type[ModelType]) -> typing.Optional[ModelType]:
        if model.__dippy_cache_type__:
            return self._get_model_from_cache(value, model)
        return self.__bevy_context__.build(model, value)

    def _get_model_from_cache(self, value: DiscordObject, model: typing.Type[ModelType]) -> typing.Optional[ModelType]:
        key = self.cache.get_key(model, value)
        ret = self.cache.get(model, *key)
        if not ret:
            self.cache.update(model, value, *key)
            ret = self.cache.get(model, *key)
        return ret

    @classmethod
    def _build_fields(cls):
        fields_ = cls._get_fields()
        cls._save_index_fields(fields_)

    @classmethod
    def _get_fields(cls) -> dict[str, fields.Field]:
        fields_ = {}
        annotations = AnnotationWrapper(cls)
        for name, annotation in cls.__annotations__.items():
            field: typing.Union[fields.Field, typing.Any] = getattr(cls, name, None)
            if not field or not isinstance(field, fields.Field):
                field = fields.Field(key_name=name, default=fields.NOTSET if field is None else field)
            elif not field.key_name:
                field.key_name = name

            field.annotation = annotations[name]
            fields_[name] = field
            setattr(cls, name, field)

        return fields_

    @classmethod
    def _save_index_fields(cls, fields: dict[str, fields.Field]):
        cls.__dippy_index_fields__ = (
            *cls.__dippy_index_fields__,
            *(name for name, field in fields.items() if field.index),
        )

    @classmethod
    def _set_cache_type(cls, cache_type: typing.Optional[str]):
        if cache_type:
            cls.__dippy_cache_type__ = cache_type


ModelType = typing.TypeVar("ModelType", bound=Model)
