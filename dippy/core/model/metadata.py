from __future__ import annotations as _
from collections import defaultdict
from typing import Generic, Protocol, Type, TypeVar


DT = TypeVar("DT", bound="MetadataDescriptorMixin")


class MetadataDict(defaultdict, Generic[DT]):
    """Default dict that uses provides methods for accessing the attributes of an object that were created using a given
    descriptor."""

    def get_for(self, obj: MetadataProtocol, descriptor: Type[DT]) -> dict[str, DT]:
        return {name: getattr(obj, name) for name in obj.__dippy_metadata__[descriptor]}


class MetadataProtocol(Protocol):
    """This protocol applies to any object that has a __dippy_metadata__ dictionary."""

    __dippy_metadata__: MetadataDict[Type[MetadataDescriptorMixin], str]


class MetadataDescriptorMixin:
    """This descriptor mixin will add the attribute name to a metadata dictionary on the owner class."""

    @classmethod
    def __set_name__(cls, owner: MetadataProtocol, name):
        if not hasattr(owner, "__dippy_metadata__"):
            owner.__dippy_metadata__ = MetadataDict(list)

        owner.__dippy_metadata__[cls].append(name)
