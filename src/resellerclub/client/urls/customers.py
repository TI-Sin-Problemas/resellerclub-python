"""Customers URL endpoints"""
from .base import BaseURLs


class CustomersURLs(BaseURLs):
    """Sets up the URLs for the customers endpoints"""

    base_url = "customers/"

    def get_search_url(self) -> str:
        """Returns the URL for the search endpoint"""
        return f"{self.base_url}search.json"
