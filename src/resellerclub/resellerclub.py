"""ResellerClub API Client"""

from .api.domains import DomainsApi


class ResellerClubAPI:
    """ResellerClub API Client"""

    def __init__(
        self,
        auth_userid: str,
        api_key: str,
        response_format: str = "json",
        debug: bool = True,
    ) -> None:

        self.domains = DomainsApi(auth_userid, api_key, response_format, debug)
