class DippyCoreBaseException(BaseException):
    """Base exception for all Dippy.core exceptions."""


class MalformedDiscordToken(DippyCoreBaseException):
    """Raised when the rest client is given a malformed Discord token."""


class NoCacheControllerFound(DippyCoreBaseException):
    """Raised when attempting to get something from the cache using a model that has no registered cache controller."""


class NotFoundInCache(DippyCoreBaseException):
    """Raised when a CacheView attempts to access an item on an object that is no longer in the cache."""