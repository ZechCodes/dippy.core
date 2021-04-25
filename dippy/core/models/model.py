from dippy.core.caching.cacheable import Cacheable
from dippy.core.timestamp import Timestamp
from pydantic import BaseModel, Field


class DippyCoreModel(BaseModel):
    pass


class DippyCoreCacheableModel(DippyCoreModel, Cacheable):
    created: Timestamp = Field(default_factory=Timestamp)
