"""Customers URL endpoints"""

from .base import BaseURLs


class CustomersURLs(BaseURLs):
    """Sets up the URLs for the customers endpoints"""

    base_url = "customers"

    @property
    def search(self) -> str:
        """Search endpoint"""
        return f"{self.base_url}/search.json"
