from __future__ import annotations
from attr import attrs
from bevy.inject import dependencies, Inject, Injectable
from collections.abc import Mapping
from dippy.core.cache.manager import CacheManager
from dippy.core.converters import build_converter, get_annotation_type
from dippy.core.not_set import NOT_SET
from typing import (
    Any,
    Generator,
    get_type_hints,
    Iterable,
    Optional,
    Sequence,
    TypeVar,
    Union,
)


Model = TypeVar("Model")


@attrs(auto_attribs=True)
class InternalField:
    name: str
    converter: Any
    value: Union[Any, NOT_SET]


@attrs(auto_attribs=True)
class Field:
    index: Optional[Sequence[str]]


@dependencies
class BaseModel:
    """Base implementation that provides all the tooling necessary to provide an efficient view of a dictionary object.

    Fields can be declared as class annotations and can be given default values through assignment. The fields will then
    be generated as properties when the class object is created. These properties will be able to reach into the data
    dictionary object to retrieve the value with the key of the same name. The value will be passed to the appropriate
    converter function for the given type annotation.
    ```py
    class MyModel(BaseModel):
        id: Snowflake
        name: str
        enabled: bool = False
    ```
    """

    cache: Inject[CacheManager]

    def __init_subclass__(cls, **kwargs):
        fields = list(cls.__get_fields())
        cls.__build_fields(fields)
        cls.__build_repr(fields)

    def __init__(self, data: Mapping):
        self._data = data

    def __repr__(self):
        """This method is built by the subclass init class hook."""

    @classmethod
    def __build_fields(cls, fields: Iterable[InternalField]):
        for field in fields:
            cls.__create_field_property(field)

    @classmethod
    def __build_repr(cls, fields: Iterable[InternalField]):
        field_strings = " ".join(
            f"{field.name}={{self.{field.name}}}" for field in fields
        )

        exec(
            f"def __repr__(self): return f'<{cls.__name__} {field_strings}>'\ncls.__repr__ = __repr__",
            {**vars(cls)},
            {"cls": cls},
        )

    @classmethod
    def __create_field_property(cls, field: InternalField):
        code = f"@property\ndef {field.name}(self):\n"
        if field.value is not NOT_SET:
            code += f"    if {field.name!r} not in self._data: return default\n"

        annotation_type, _ = get_annotation_type(field.converter)
        if isinstance(annotation_type, type) and issubclass(annotation_type, BaseModel):
            index = "data['id']"
            if isinstance(field.value, Field):
                _index = [
                    v
                    for idx in field.value.index.split(".")
                    if (v := cls.__convert_dot_path_to_dict_lookup(idx))
                ]
                if _index:
                    index = ", ".join(_index)

            code += (
                f"    data = self._data.get({field.name!r})\n"
                f"    return self.cache.get(model_type, {index})"
            )
        else:
            code += f"    return converter(self._data.get({field.name!r}))"

        if field.value is NOT_SET:
            code += f"if {field.name!r} in self._data else None"

        code += f"\ncls.{field.name} = {field.name}"

        exec(
            code,
            {
                "default": field.value,
                "converter": build_converter(field),
                "model_type": annotation_type,
                **vars(cls),
            },
            {"cls": cls},
        )

    @classmethod
    def __get_fields(cls) -> Generator[InternalField, None, None]:
        for name, annotation in get_type_hints(cls).items():
            if cls.__allowed_field(annotation):
                yield InternalField(name, annotation, getattr(cls, name, NOT_SET))

    @classmethod
    def __allowed_field(cls, annotation_type: Any) -> bool:
        """Ignore anything that relies on Bevy."""
        return not isinstance(annotation_type, Injectable) or (
            isinstance(annotation_type, type)
            and issubclass(annotation_type, Injectable)
        )

    @staticmethod
    def __convert_dot_path_to_dict_lookup(dot_path: str) -> Optional[str]:
        result = []
        for item in dot_path.split("."):
            if not item.isidentifier():
                return
            result.append(f"[{item!r}]")

        return "".join(result)
