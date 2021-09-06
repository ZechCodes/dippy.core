class DippyCoreBaseException(BaseException):
    """Base exception for all Dippy.core exceptions."""


class MalformedDiscordToken(DippyCoreBaseException):
    """Raised when the rest client is given a malformed Discord token."""
