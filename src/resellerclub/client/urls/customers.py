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

    @property
    def details_by_username(self) -> str:
        """Endpoint to get customer details by username"""
        return f"{self.base_url}/details.json"

    @property
    def details_by_id(self) -> str:
        """Endpoint to get customer details by ID"""
        return f"{self.base_url}/details-by-id.json"

    @property
    def modify(self) -> str:
        """Endpoint to modify customer details"""
        return f"{self.base_url}/modify.json"

    @property
    def generate_token(self) -> str:
        """Endpoint to generate a token for a customer"""
        return f"{self.base_url}/generate-token.json"

    @property
    def generate_login_token(self) -> str:
        """Endpoint to generate a login token for a customer"""
        return f"{self.base_url}/generate-login-token.json"

    @property
    def authenticate_token(self) -> str:
        """Endpoint to authenticate a token for a customer"""
        return f"{self.base_url}/authenticate-token.json"

    @property
    def change_password(self) -> str:
        """Endpoint to change a customer's password"""
        return f"{self.base_url}/change-password.json"

    @property
    def forgot_password(self) -> str:
        """Endpoint to change a customer's password"""
        return f"{self.base_url}/forgot-password.json"

    @property
    def delete(self) -> str:
        """Endpoint to delete a customer"""
        return f"{self.base_url}/delete.json"
