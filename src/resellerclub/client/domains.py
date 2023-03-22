"""Domains API Client"""
from typing import List, NamedTuple

from .base import BaseClient


class Availability(NamedTuple):
    """Domain name availability for TLDs"""

    domain: str
    status: str
    classkey: str = None


class PremiumDomain(NamedTuple):
    """Premium Domain"""

    domain: str
    price: float


class Suggestion(NamedTuple):
    """Domain name suggestion"""

    domain: str
    status: str
    in_ga: bool
    score: float
    spin: str


class DomainsClient(BaseClient):
    """Domains API Client. Methods to Search, Register or Renew domain names, etc."""

    def check_availability(self, domain_names: list, tlds: list) -> List[Availability]:
        """Checks the availability of the specified domain name(s).
        https://manage.resellerclub.com/kb/answer/764

        Args:
            domain_names (list): Domain name(s) that you need to check the availability for
            tlds (list): TLDs for which the domain name availability needs to be checkedW

        Returns:
            List[Availability]: Returns a list containing domain name availability status for the
            requested TLDs
        """
        params = {"domain-name": domain_names, "tlds": tlds}
        url = self._urls.domains.get_availability_check_url()
        data = self._get_data(url, params)

        return [Availability(dn, **a) for dn, a in data.items() if not dn == "errors"]

    def check_idn_availability(
        self, domain_names: list, tld: str, idn_language_code: str
    ) -> List[Availability]:
        """Checks the availability of the specified Internationalized Domain Name(s) (IDN)
        https://manage.resellerclub.com/kb/answer/1427

        Args:
            domain_names (list): Internationalized Domaine Name(s) that you need to check the
            availability for
            tld (str): TLD for which the domain name availability needs to be checked
            idn_language_code (str): While performing check availability for an Internationalized
            Domain Name, you need to provide the corresponding language code

        Returns:
            List[Availability]: List containing domain name availability status for the requested
            TLDs
        """
        params = {
            "domain-name": domain_names,
            "tld": tld,
            "idnLanguageCode": idn_language_code,
        }
        url = self._urls.domains.get_availability_check_url("idn")
        data = self._get_data(url, params)

        return [Availability(dn, **availability) for dn, availability in data.items()]

    def check_premium_domain_availability(
        self,
        keyword: str,
        tlds: list,
        highest_price: int = None,
        lowest_price: int = None,
        max_results: int = None,
    ) -> List[PremiumDomain]:
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
            List[PremiumDomain]: List of domain names and prices
        """

        params = {
            "key-word": keyword,
            "tlds": tlds,
            "price-high": highest_price,
            "price-low": lowest_price,
            "no-of-results": max_results,
        }
        url = self._urls.domains.get_availability_check_url("premium")
        data = self._get_data(url, params)

        return [PremiumDomain(domain, float(price)) for domain, price in data.items()]

    def check_third_level_name_availability(
        self, domain_names: list
    ) -> List[Availability]:
        """Checks the availability of the specified 3rd level .NAME domain name(s).
        https://manage.resellerclub.com/kb/node/2931

        Args:
            domain_names (list): Domain name(s) that you need to check the availability for.

        Returns:
            List[Availability]: List containing domain name availability status for the requested
            domain names
        """
        params = {"domain-name": domain_names, "tlds": "*.name"}
        url = self._urls.domains.get_availability_check_url("3rd_level_dotname")
        data = self._get_data(url, params)

        return [Availability(dn, **availability) for dn, availability in data.items()]

    def suggest_names(
        self,
        keyword: str,
        tld_only: str = None,
        exact_match: bool = None,
        adult: bool = None,
    ) -> List[Suggestion]:
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
            List[Suggestion]: List of domain name suggestions.
        """
        params = {
            "keyword": keyword,
            "tld-only": tld_only,
            "exact-match": exact_match,
            "adult": adult,
        }
        url = self._urls.domains.get_name_suggestion_url()
        data = self._get_data(url, params)

        result = []
        for domain, sug in data.items():
            in_ga = bool(sug["in_ga"].lower() == "true")
            score = float(sug["score"])
            suggestion_params = [domain, sug["status"], in_ga, score, sug["spin"]]
            result.append(Suggestion(*suggestion_params))

        return result
