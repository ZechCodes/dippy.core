from __future__ import annotations as _
from dippy.core.model.fields import Field, NOTSET
from dippy.core.model.models import Model
from dippy.core.model.metadata import MetadataProtocol
from typing import Any, Optional, Type


class DataModel(Model, MetadataProtocol):
    endpoint: str
    method: str
    model: Optional[Model] = None

    def __init__(self, *args, **kwargs):
        super().__init__(self._load_fields(*args, **kwargs))

    @property
    def fields(self) -> dict[str, Any]:
        return self.__dippy_metadata__.get_for(self, Field)

    def _get_field_args(
        self,
        descriptor: Type[Field],
        args: tuple[Any],
        kwargs: dict[str, Any],
        *,
        allow_positional: bool = False,
        index: int = 0,
    ) -> dict[str, Any]:
        values = {}
        for name in self.__dippy_metadata__[descriptor]:
            field: Field = getattr(type(self), name)
            if name in kwargs:
                value = kwargs[name]
            elif not field.kw_only and allow_positional and index < len(args):
                value = args[index]
                index += 1
            elif field.default is not NOTSET:
                value = field.default
            elif field.factory:
                value = field.factory()
            elif field.is_optional:
                continue
            else:
                raise TypeError(
                    f"{type(self).__qualname__} missing 1 required positional argument: '{name}'\n    {args=}\n    "
                    f"{kwargs=}\n    {type(self)=}\n    {field=}\n    {allow_positional=}\n    {index=}"
                )

            values[name] = value

        return values

    def _load_fields(self, *args, **kwargs) -> dict[str, Any]:
        return self._get_field_args(Field, args, kwargs, allow_positional=True)
