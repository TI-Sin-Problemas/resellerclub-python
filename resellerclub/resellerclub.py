"""ResellerClub API Client"""
from typing import Union
from xml.etree import ElementTree
import requests
from .urls import URLs


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

    def __to_format(
        self, response: requests.Response
    ) -> Union[dict, ElementTree.Element]:
        """Returns response parsed as dict from JSON or XML Element

        Args:
            response (requests.Response): Response from requests.get method

        Returns:
            dict | ElementTree.Element: dict from JSON response or hash map from XML response
        """
        if self.response_format == "xml":
            return ElementTree.fromstring(response.content)

        return response.json()

    def __get_data(
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
        return self.__to_format(requests.get(url, full_params))

    def check_domain_availability(
        self, domain_names: list, tlds: list
    ) -> Union[dict, ElementTree.Element]:
        """Checks the availability of the specified domain name(s).
        https://manage.resellerclub.com/kb/answer/764

        Args:
            domain_names (list): Domain name(s) that you need to check the availability for
            tlds (list): TLDs for which the domain name availability needs to be checkedW

        Returns:
            dict | ElementTree.Element: Returns a hash map or dict containing domain name
            availability status for the requested TLDs
        """
        params = {"domain-name": domain_names, "tlds": tlds}
        url = self.urls.domains_availability_url()

        return self.__get_data(url, params)

    def check_domain_availability_idn(
        self, domain_names: list, tld: str, idn_language_code: str
    ) -> Union[dict, ElementTree.Element]:
        """Checks the availability of the specified Internationalized Domain Name(s) (IDN)
        https://manage.resellerclub.com/kb/answer/1427

        Args:
            domain_names (list): Internationalized Domaine Name(s) that you need to check the
            availability for
            tld (str): TLD for which the domain name availability needs to be checked
            idn_language_code (str): While performing check availability for an Internationalized
            Domain Name, you need to provide the corresponding language code

        Returns:
            dict | ElementTree.Element: Returns a dict or hash map containing domain name
            availability status for the requested TLDs
        """
        params = {
            "domain-name": domain_names,
            "tld": tld,
            "idnLanguageCode": idn_language_code,
        }
        url = self.urls.domains_idn_availability_url()

        return self.__get_data(url, params)
