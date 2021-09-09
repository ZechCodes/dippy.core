from collections.abc import Mapping
from dippy.core.cache.controller import CacheController
from dippy.core.exceptions import NotFoundInCache


class CacheView(Mapping):
    def __init__(self, controller: CacheController, *args):
        self._controller = controller
        self._id_lookup = args

    @property
    def data(self):
        data = self._controller.get(*self._id_lookup)
        if data is None:
            raise NotFoundInCache(
                f"The {self._controller!r} was unable to find an object matching {self._id_lookup!r}"
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
