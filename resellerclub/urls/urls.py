"""ResellerClub API URLs"""


from resellerclub.urls.base import BaseURLs
from resellerclub.urls.domains import DomainsURLs


class URLs(BaseURLs):
    """Stores all API URLs"""

    prod_url = "https://httpapi.com/api/"
    test_url = "https://test.httpapi.com/api/"

    def __init__(self, debug: bool = True, response_format: str = "json") -> None:
        """Stores all API URLs

        Args:
            debug (bool, optional): Use the test or live API URLs. Defaults to True.
            response_format (str, optional): Valid values are json or xml. Defaults to "json".
        """
        base_url = self.test_url if debug else self.prod_url
        super().__init__(base_url, response_format)

        # Domains urls
        self.domains = DomainsURLs(self.base_url, response_format)
