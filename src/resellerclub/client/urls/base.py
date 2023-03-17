"""Base URL Classes"""


class BaseURLs:
    """URLs base class"""

    base_url = ""

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self}>"

    def __str__(self) -> str:
        return self.base_url

    def __init__(self, base_url: str = "") -> None:
        """Stores URLs

        Args:
            base_url (str, optional): Base url for all the endpoints. Defaults to "".
            response_format (str, optional): Valid values are json or xml. Defaults to "json".
        """
        self.base_url = f"{base_url}{self.base_url}"
