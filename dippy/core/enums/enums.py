import enum as _enum


class MissingEnum:
    @classmethod
    def _missing_(cls, key):
        if hasattr(cls, "UNKNOWN_VALUE"):
            return cls.UNKNOWN_VALUE


class Enum(MissingEnum, _enum.Enum):
    def __str__(self):
        return str(self._value_)


class IntEnum(int, Enum):
    ...


class StrEnum(str, Enum):
    ...
