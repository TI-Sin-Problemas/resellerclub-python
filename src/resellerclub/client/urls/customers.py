"""Customers URL endpoints"""

from .base import BaseURLs


class CustomersURLs(BaseURLs):
    """Sets up the URLs for the customers endpoints"""

    base_url = "customers"

    @property
    def signup(self) -> str:
        """Sign up endpoint"""
        return f"{self.base_url}/signup.json"

    @property
    def search(self) -> str:
        """Search endpoint"""
        return f"{self.base_url}/search.json"
