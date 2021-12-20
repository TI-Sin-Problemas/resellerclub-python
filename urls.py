"""ResellerClub API URLs"""


class URLs:
    """Stores all API URLs"""

    prod_url = "https://httpapi.com/api/"
    test_url = "https://test.httpapi.com/api/"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self}>"

    def __str__(self) -> str:
        return self.base_url

    def __init__(self, debug: bool = True, response_format: str = "json") -> None:
        """Stores all API URLs

        Args:
            debug (bool, optional): Use the test or live API URLs. Defaults to True.
            response_format (str, optional): Valid values are json or xml. Defaults to "json".
        """
        self.base_url = self.test_url if debug else self.prod_url
        self.format = response_format

        # Domains urls
        self.domains_url = "domains/"

    def domains_availability_url(self):
        return f"{self.base_url}{self.domains_url}available.{self.format}"
