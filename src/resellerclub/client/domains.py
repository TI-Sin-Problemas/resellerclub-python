from typing import Dict, NamedTuple, Union
from xml.etree import ElementTree

from .base import BaseClient


class Availability(NamedTuple):
    """Domain name availability for TLDs"""

    status: str
    classkey: str = None


class DomainsClient(BaseClient):
    """Domains API Client. Methods to Search, Register or Renew domain names, etc."""

    def check_availability(
        self, domain_names: list, tlds: list
    ) -> Dict[str, Availability]:
        """Checks the availability of the specified domain name(s).
        https://manage.resellerclub.com/kb/answer/764

        Args:
            domain_names (list): Domain name(s) that you need to check the availability for
            tlds (list): TLDs for which the domain name availability needs to be checkedW

        Returns:
            Dict[str, Availability]: Returns a dict containing domain name availability status
            for the requested TLDs
        """
        params = {"domain-name": domain_names, "tlds": tlds}
        url = self.urls.domains.check_availability()
        data = self._get_data(url, params)

        return {
            domain: Availability(**availability)
            for domain, availability in data.items()
        }

    def check_idn_availability(
        self, domain_names: list, tld: str, idn_language_code: str
    ) -> Dict[str, Availability]:
        """Checks the availability of the specified Internationalized Domain Name(s) (IDN)
        https://manage.resellerclub.com/kb/answer/1427

        Args:
            domain_names (list): Internationalized Domaine Name(s) that you need to check the
            availability for
            tld (str): TLD for which the domain name availability needs to be checked
            idn_language_code (str): While performing check availability for an Internationalized
            Domain Name, you need to provide the corresponding language code

        Returns:
            Dict[str, Availability]: Returns a dict containing domain name availability status for
            the requested TLDs
        """
        params = {
            "domain-name": domain_names,
            "tld": tld,
            "idnLanguageCode": idn_language_code,
        }
        url = self.urls.domains.check_idn_availability()
        data = self._get_data(url, params)

        return {
            domain: Availability(**availability)
            for domain, availability in data.items()
        }

    def check_premium_domain_availability(
        self,
        keyword: str,
        tlds: list,
        highest_price: int = None,
        lowest_price: int = None,
        max_results: int = None,
    ) -> Dict[str, float]:
        """Returns a list of Aftermarket Premium domain names based on the specified keyword.
        This method only returns names available on the secondary market, and not those premium
        names that are offered directly by any Registry for new registration.
        https://manage.resellerclub.com/kb/answer/1948

        Args:
            keyword (str): Word or phrase (please enter the phrase without spaces) for which
            premium search is requested
            tlds (list): Domain name extensions (TLDs) you want to search in
            highest_price (int, optional): Maximum price (in Reseller's Selling Currency) up to
            which domain names must be suggested. Defaults to None.
            lowest_price (int, optional): Minimum price (in Reseller's Selling Currency) for which
            domain names must be suggested. Defaults to None.
            max_results (int, optional): Number of results to be returned. Defaults to None.

        Returns:
            Dict[str, float]: Dictionary of domain names and prices
        """

        params = {
            "key-word": keyword,
            "tlds": tlds,
            "price-high": highest_price,
            "price-low": lowest_price,
            "no-of-results": max_results,
        }
        url = self.urls.domains.check_premium_availability()
        data = self._get_data(url, params)

        return {domain: float(price) for domain, price in data.items()}

    def check_third_level_name_availability(
        self, domain_names: list
    ) -> Dict[str, Availability]:
        """Checks the availability of the specified 3rd level .NAME domain name(s).
        https://manage.resellerclub.com/kb/node/2931

        Args:
            domain_names (list): Domain name(s) that you need to check the availability for.

        Returns:
            Dict[str, Availability]: Dictionary containing domain name availability status for the
            requested TLDs.
        """
        params = {"domain-name": domain_names, "tlds": "*.name"}
        url = self.urls.domains.check_third_level_name_availability()
        data = self._get_data(url, params)

        return {
            domain: Availability(**availability)
            for domain, availability in data.items()
        }

    def suggest_names(
        self,
        keyword: str,
        tld_only: str = None,
        exact_match: bool = None,
        adult: bool = None,
    ) -> Union[dict, ElementTree.Element]:
        """Returns domain name suggestions for a user-specified keyword.
        https://manage.resellerclub.com/kb/answer/1085

        Args:
            keyword (str): Search term (keyword or phrase) e.g. "search" or "search world"
            tld_only (str, optional): Specific TLD(s) you may want to search for. Defaults to None.
            exact_match (bool, optional): Will return keyword alternatives when set to True.
            Can be set to False to only return TLD alternatives. Defaults to None.
            adult (bool, optional): If set to false, the suggestions will not contain any adult or
            explicit suggestions which contain words like "nude", "porn", etc. Defaults to None.

        Returns:
            Union[dict, ElementTree.Element]: Dict or hash map containing availability status of suggested domain names for the keyword supplied.
        """
        params = {
            "keyword": keyword,
            "tld-only": tld_only,
            "exact-match": exact_match,
            "adult": adult,
        }
        url = self.urls.domains.suggest_names()

        return self._get_data(url, params)
