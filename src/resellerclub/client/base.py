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

    def _build_params(self, **kwargs) -> dict:
        params = {"auth-userid": self._auth_userid, "api-key": self._api_key}
        params.update(kwargs)
        return params

    def _perform_request(self, method: str, url: str, params: dict) -> dict:
        """Perform a request to the API.

        Args:
            method (str): Request method. Valid values are get, post, put, delete.
            url (str): URL to request.
            params (dict): Parameters to send in the request.

        Returns:
            dict: dict with response data
        """
        params = self._build_params(**params)
        func = getattr(requests, method)
        response = func(url, params, timeout=120)

        try:
            data = response.json()
        except requests.JSONDecodeError:
            response.raise_for_status()

        if not response.ok:
            raise ResellerClubAPIException(data["message"])

        return data

    def get(self, url: str, params: dict) -> requests.Response:
        """Perform a GET request to the API

        Args:
            url (str): URL to request data from
            params (dict, optional): Parameters to send in the query string.

        Returns:
            dict: dict with response data
        """
        return self._perform_request("get", url, params)

    def post(self, url: str, params: dict) -> requests.Response:
        """Perform a POST request to the API

        Args:
            url (str): URL to send the request to
            params (dict, optional): Parameters to send in the request body.

        Returns:
            dict: dict with response data
        """
        return self._perform_request("post", url, params)
