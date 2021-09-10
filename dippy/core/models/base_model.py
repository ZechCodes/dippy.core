from attr import attrs
from collections.abc import Mapping
from dippy.core.converters import build_converter
from dippy.core.not_set import NOT_SET
from enum import Enum
from inspect import getmodule
from typing import Any, Generator, get_type_hints, get_origin, Iterable, Union


@attrs(auto_attribs=True)
class Field:
    name: str
    converter: Any
    value: Union[Any, NOT_SET]


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

    def __init_subclass__(cls, **kwargs):
        fields = list(cls.__get_fields())
        cls.__build_fields(fields)
        cls.__build_repr(fields)

    def __init__(self, data: Mapping):
        self._data = data

    def __repr__(self):
        """This method is built by the subclass init class hook."""

    @classmethod
    def __build_fields(cls, fields: Iterable[Field]):
        for field in fields:
            cls.__create_field_property(field)

    @classmethod
    def __build_repr(cls, fields: Iterable[Field]):
        field_strings = " ".join(f"{{self.{field.name}=}}" for field in fields)

        exec(
            f"def __repr__(self): return f'<{cls.__name__} {field_strings}>'\ncls.__repr__ = __repr__",
            {**vars(cls)},
            {"cls": cls},
        )

    @classmethod
    def __create_field_property(cls, field: Field):
        code = f"@property\ndef {field.name}(self):\n"
        if field.value is not NOT_SET:
            code += f"    if {field.name!r} not in self._data: return default\n"
        code += f"    return converter(self._data.get({field.name!r}))"
        if field.value is NOT_SET:
            code += f"if {field.name!r} in self._data else None"
        code += f"\ncls.{field.name} = {field.name}"

        exec(
            code,
            {"default": field.value, "converter": build_converter(field), **vars(cls)},
            {"cls": cls},
        )

    @classmethod
    def __get_fields(cls) -> Generator[Field, None, None]:
        for name, annotation in get_type_hints(cls).items():
            if cls.__allowed_field(annotation):
                yield Field(name, annotation, getattr(cls, name, NOT_SET))

    @classmethod
    def __allowed_field(cls, annotation_type: Any) -> bool:
        """Only allow fields that are attrs classes, models, enums, special annotations, or builtins."""
        if hasattr(annotation_type, "__attrs_attrs__"):
            return True

        if issubclass(annotation_type, (BaseModel, Enum)):
            return True

        if get_origin(annotation_type):
            return True

        return getmodule(annotation_type) is getmodule(dict)
