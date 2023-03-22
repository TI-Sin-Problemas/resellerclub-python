"""Base API classes"""
import requests

from ..exceptions import ResellerClubAPIException
from .urls import URLs


class BaseClient:
    """Base API Client class"""

    def __init__(
        self,
        auth_userid: str,
        api_key: str,
        test_mode: bool = True,
    ) -> None:
        self._auth_userid = auth_userid
        self._api_key = api_key
        self._urls = URLs(test_mode)

    def _get_data(self, url: str, params: dict = None) -> dict:
        """Get response from API

        Args:
            url (str): URL to request data from
            params (dict, optional): Parameters of the request. Defaults to None.

        Returns:
            dict: dict with response data
        """
        params.update({"auth-userid": self._auth_userid, "api-key": self._api_key})
        response = requests.get(url, params, timeout=120)

        try:
            data = response.json()
        except requests.JSONDecodeError:
            response.raise_for_status()

        if not response.ok:
            raise ResellerClubAPIException(data["message"])

        return data
