"""ResellerClub API URLs"""


from .base import BaseURLs
from .domains import DomainsURLs
from .customers import CustomersURLs


class URLs(BaseURLs):
    """Stores all API URLs"""

    prod_url = "https://httpapi.com/api/"
    test_url = "https://test.httpapi.com/api/"

    def __init__(self, test_mode: bool = True) -> None:
        """Stores all API URLs

        Args:
            debug (bool, optional): Use the test or live API URLs. Defaults to True.
            response_format (str, optional): Valid values are json or xml. Defaults to "json".
        """
        base_url = self.test_url if test_mode else self.prod_url
        super().__init__(base_url)

        # Domains urls
        self.domains = DomainsURLs(self.base_url)
        self.customers = CustomersURLs(self.base_url)
