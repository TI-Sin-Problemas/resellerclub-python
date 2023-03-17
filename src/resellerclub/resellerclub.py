"""ResellerClub API Client"""

from .api.domains import DomainsClient


class ResellerClubAPI:
    """ResellerClub API Client"""

    def __init__(
        self,
        auth_userid: str,
        api_key: str,
        response_format: str = "json",
        test_mode: bool = True,
    ) -> None:

        self.domains = DomainsClient(auth_userid, api_key, response_format, test_mode)
