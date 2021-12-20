from xml.etree import ElementTree
import requests
from urls import URLs


class ResellerClubAPI:
    """ResellerClub API"""

    def __init__(
        self,
        auth_userid: str,
        api_key: str,
        response_format: str = "json",
        debug: bool = True,
    ) -> None:
        self.auth_userid = auth_userid
        self.api_key = api_key
        self.response_format = response_format
        self.urls = URLs(debug, response_format)

    def __add_auth(self, params: dict) -> dict:
        """Adds auth data to request params

        Returns:
            dict: Dictionary to be used as params on request
        """
        auth_dict = {"auth-userid": self.auth_userid, "api-key": self.api_key}

        return {**params, **auth_dict}

    def __to_format(self, response):
        if self.response_format == "json":
            return response.json()
        else:
            return ElementTree.fromstring(response.content)

    def __get_data(self, url, params: dict = None):
        full_params = self.__add_auth(params)
        return self.__to_format(requests.get(url, full_params))

