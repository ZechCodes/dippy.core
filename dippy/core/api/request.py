from __future__ import annotations as _
from dippy.core.model.fields import Field as _Field, NOTSET as _FIELD_NOTSET
from dippy.core.model.models import Model as _Model
from dippy.core.model.metadata import MetadataProtocol as _MetadataProtocol
from dippy.core.sentinel import Sentinel as _Sentinel
from typing import Any as _Any, Optional as _Optional


NOTSET = _Sentinel("NOTSET")


class JSONArgField(_Field):
    ...


class QueryArgField(_Field):
    ...


class URLArgField(_Field):
    ...


class RequestModel(_Model):
    endpoint: str
    method: str
    model: _Optional[_Model] = None

    def __init__(self: _MetadataProtocol, *args, **kwargs):
        state = {
            **self._get_field_args(JSONArgField, args, kwargs),
            **self._get_field_args(QueryArgField, args, kwargs),
            **self._get_field_args(URLArgField, args, kwargs, allow_positional=True),
        }
        super().__init__(state)

    @property
    def json_args(self: _MetadataProtocol) -> dict[str, _Any]:
        return self.__dippy_metadata__.get_for(self, JSONArgField)

    @property
    def query_args(self: _MetadataProtocol) -> dict[str, _Any]:
        return self.__dippy_metadata__.get_for(self, QueryArgField)

    @property
    def url_args(self: _MetadataProtocol) -> dict[str, _Any]:
        return self.__dippy_metadata__.get_for(self, URLArgField)

    def _get_field_args(
        self: _MetadataProtocol,
        descriptor: _Field,
        args: tuple[_Any],
        kwargs: dict[str, _Any],
        *,
        allow_positional: bool = False,
        index: int = 0,
    ) -> dict[str, _Any]:
        values = {}
        for name in self.__dippy_metadata__[descriptor]:
            field: URLArgField = getattr(type(self), name)
            if name in kwargs:
                value = kwargs[name]
            elif allow_positional and index < len(args):
                value = args[index]
                index += 1
            elif field.default is not _FIELD_NOTSET:
                value = field.default
            else:
                raise TypeError(
                    f"__init__() missing 1 required positional argument: '{name}'"
                )

            values[name] = value

        return values
