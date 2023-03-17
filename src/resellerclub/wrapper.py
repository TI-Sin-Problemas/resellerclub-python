"""ResellerClub API Client"""

from .client.domains import DomainsClient


class ResellerClubAPI:
    """ResellerClub API Client"""

    def __init__(
        self,
        auth_userid: str,
        api_key: str,
        test_mode: bool = True,
    ) -> None:

        self.domains = DomainsClient(auth_userid, api_key, test_mode)
