"""ResellerClub API Client"""

from .client.customers import CustomersClient
from .client.domains import DomainsClient


class ResellerClub:
    """ResellerClub API Client"""

    def __init__(
        self,
        auth_userid: str,
        api_key: str,
        test_mode: bool = True,
    ) -> None:

        self.domains = DomainsClient(auth_userid, api_key, test_mode)
        self.customers = CustomersClient(auth_userid, api_key, test_mode)
