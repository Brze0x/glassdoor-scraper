from typing import Optional


class GlassdoorScraperException(Exception):
    """
    Base GlassdoorScraper exception.
    """

    def __init__(self, msg: Optional[str] = None) -> None:
        self.msg = msg

    def __str__(self) -> str:
        return "Message: %s\n" % self.msg


class InvalidInputError(GlassdoorScraperException):
    """
    Thrown when the user entered invalid input data.
    """
