from collections.abc import Mapping
from dippy.core.cache.cache import CacheProtocol
from dippy.core.exceptions import NotFoundInCache
from dippy.core.snowflake import Snowflake
from typing import Union


class CacheView(Mapping):
    def __init__(
        self, cache: CacheProtocol, id_lookup: tuple[Union[str, int, Snowflake]]
    ):
        self._cache = cache
        self._id_lookup = args

    @property
    def data(self):
        data = self._cache.get(self._id_lookup)
        if data is None:
            raise NotFoundInCache(
                f"The {self._cache!r} was unable to find an object matching {self._id_lookup!r}"
            )
        return data

    def __getitem__(self, item):
        return self.data[item]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        try:
            return len(self.data)
        except NotFoundInCache:
            return 0
