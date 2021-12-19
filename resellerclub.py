from .urls import URLs


class ResellerClubAPI:
    """ResellerClub API"""

    def __init__(
        self,
        auth_userid: str,
        token: str,
        response_format: str = "json",
        debug: bool = True,
    ) -> None:
        self.auth_userid = auth_userid
        self.token = token
        self.response_format = response_format
        self.urls = URLs(debug)
