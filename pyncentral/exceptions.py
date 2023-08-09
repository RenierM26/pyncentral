"""pyNCentral Exceptions."""


class NCentralError(Exception):
    """pyNCentral Exception class."""


class InvalidURL(NCentralError):
    """Invalid url exception."""


class HTTPError(NCentralError):
    """Invalid host exception."""
