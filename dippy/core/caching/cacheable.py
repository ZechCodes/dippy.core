from __future__ import annotations
from abc import ABC, abstractmethod
from dippy.core.timestamp import Timestamp


class Cacheable(ABC):
    # @abstractmethod
    def update(self, payload: Cacheable):
        ...

    def __eq__(self, other):
        return isinstance(other, Cacheable) and hash(self) == hash(other)

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"<{type(self).__name__} {self.id}>"
