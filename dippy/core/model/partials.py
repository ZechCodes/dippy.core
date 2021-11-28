from typing import Protocol, runtime_checkable


class Partial(Protocol):
    def __init_subclass__(cls, **kwargs):
        runtime_checkable(cls)
