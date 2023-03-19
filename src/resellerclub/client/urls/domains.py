"""Domains URL endpoints"""
from typing import Literal

from .base import BaseURLs


class DomainsURLs(BaseURLs):
    """Stores all API URLs to search, register or renew domain names"""

    base_url = "domains/"

    def get_availability_check_url(
        self, domain_type: Literal["idn", "premium", "3rd_level_dotname"] = None
    ) -> str:
        """Returns URL for domain availability check

        Args:
            domain_type: Type of domain to check.
                "idn": Internationalized Domain Name availability check.
                "premium": Premium Domain Availability check.
                "3rd_level_dotname": 3rd level .NAME availability check.
                None: Regular domain availability check.
                Defaults to None.

        Returns:
            str: API endpoint URL
        """

        url_map = {
            "idn": f"{self.base_url}idn-available.json",
            "premium": f"{self.base_url}premium/available.json",
            "3rd_level_dotname": f"{self.base_url}thirdlevelname/available.json",
        }

        return url_map.get(domain_type, f"{self.base_url}available.json")

    def get_name_suggestion_url(self) -> str:
        """Returns URL for domain name suggestion

        Returns:
            str: API endpoint URL
        """
        return f"{self.base_url}v5/suggest-names.json"
