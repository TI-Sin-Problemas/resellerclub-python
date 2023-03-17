"""Base API classes"""
from typing import Union
from xml.etree import ElementTree

import requests

from .urls import URLs


class BaseClient:
    """Base API Client class"""

    def __init__(
        self,
        auth_userid: str,
        api_key: str,
        test_mode: bool = True,
    ) -> None:
        self.auth_userid = auth_userid
        self.api_key = api_key
        self.urls = URLs(test_mode)

    def __add_auth(self, params: dict) -> dict:
        """Adds auth data to request params

        Returns:
            dict: Dictionary to be used as params on request
        """
        auth_dict = {"auth-userid": self.auth_userid, "api-key": self.api_key}

        return {**params, **auth_dict}

    def _get_data(
        self, url: str, params: dict = None
    ) -> Union[dict, ElementTree.Element]:
        """Get response from API

        Args:
            url (str): URL to request data from
            params (dict, optional): Parameters of the request. Defaults to None.

        Returns:
            dict | ElementTree.Element: dict or hash map with response data
        """
        full_params = self.__add_auth(params)
        response = requests.get(url, full_params, timeout=120)

        return response.json()
