class Sentinel:
    def __init__(self, name: str, truthy: bool = False):
        self._name = name
        self._truthy = truthy

    def __repr__(self):
        return f"{type(self).__name__}[{self._name}]"

    def __bool__(self):
        return self._truthy
