"""ResellerClub API URLs"""


class URLs:
    """Stores all API URLs"""

    prod_url = "https://httpapi.com/"
    test_url = "https://test.httpapi.com/"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self}"

    def __str__(self) -> str:
        return self.base_url

    def __init__(self, debug: bool = True) -> None:
        self.base_url = self.test_url if debug else self.prod_url
