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
        """Domain availability check URL"""
        return f"{self.base_url}{self.domains_url}available.{self.format}"

    def domains_idn_availability_url(self):
        """Internationalized Domain Name availability check URL"""
        return f"{self.base_url}{self.domains_url}idn-available.{self.format}"

    def domains_premium_availability_url(self):
        """Premium domain availability check URL"""
        return f"{self.base_url}{self.domains_url}premium/available.{self.format}"

    def domains_third_level_name_availability_url(self):
        """3rd level .NAME availability check URL"""
        return (
            f"{self.base_url}{self.domains_url}thirdlevelname/available.{self.format}"
        )
