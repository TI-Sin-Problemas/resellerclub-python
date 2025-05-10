"""Customers Unit Tests"""

import uuid

import pytest
import requests

from src.resellerclub import ResellerClub
from src.resellerclub.models import customer as customer_models


class MockRequests:
    """Mock Requests class"""

    def __init__(self, response_content: bytes):
        r = requests.Response()
        r.encoding = "UTF-8"
        r.status_code = 200
        r._content = response_content
        self.response = r

    def get(self, *args, **kwargs):  # pylint: disable=unused-argument
        """Get mock response from API"""
        return self.response

    def post(self, *args, **kwargs):  # pylint: disable=unused-argument
        """Post mock response from API"""
        return self.response


@pytest.mark.usefixtures("api_class")
class TestSearchCustomers:
    """Test SearchCustomers"""

    api: ResellerClub

    def test_sign_up_customer(self, monkeypatch):
        """Test sign up a new customer"""
        with open("tests/responses/customers/sign_up.txt", "rb") as f:
            content = f.read()
        mock = MockRequests(response_content=content)
        monkeypatch.setattr(requests, "post", mock.post)

        new_customer = customer_models.NewCustomer(
            username="email@email.com",
            password="password9",
            name="Customer Name",
            company="Customer Company",
            address=customer_models.Address(
                line1="Customer Address",
                city="City",
                state="State",
                country="US",
                zip_code="12345",
            ),
            phones=customer_models.CustomerPhones(
                phone_country_code="1",
                phone="1234567890",
            ),
            language_code="en",
        )

        customer_id = self.api.customers.sign_up(new_customer)

        assert isinstance(customer_id, int)

    def test_search_first_ten_customers(self, monkeypatch):
        """Test search first ten customers"""
        with open("tests/responses/customers/customers.txt", "rb") as f:
            response_content = f.read()
        mock = MockRequests(response_content=response_content)
        monkeypatch.setattr(requests, "get", mock.get)

        customers = self.api.customers.search(10, 1)
        assert all(isinstance(c, customer_models.Customer) for c in customers)
        assert all(isinstance(c.address, customer_models.Address) for c in customers)
        assert all(
            isinstance(c.phones, customer_models.CustomerPhones) for c in customers
        )

    def test_get_customer_by_username(self, monkeypatch):
        """Test get customer by username"""
        with open("tests/responses/customers/customer_details.txt", "rb") as f:
            response_content = f.read()
        mock = MockRequests(response_content=response_content)
        monkeypatch.setattr(requests, "get", mock.get)

        customer = self.api.customers.get_by_username("email@email.com")
        assert isinstance(customer, customer_models.Customer)
        assert isinstance(customer.address, customer_models.Address)
        assert isinstance(customer.phones, customer_models.CustomerPhones)

    def test_get_customer_by_id(self, monkeypatch):
        """Test get customer by ID"""
        with open("tests/responses/customers/customer_details.txt", "rb") as f:
            response_content = f.read()
        mock = MockRequests(response_content=response_content)
        monkeypatch.setattr(requests, "get", mock.get)

        customer = self.api.customers.get_by_id(30930235)
        assert isinstance(customer, customer_models.Customer)
        assert isinstance(customer.address, customer_models.Address)

    def test_modify_customer(self, monkeypatch):
        """Test modify customer"""
        with open("tests/responses/customers/customer_details.txt", "rb") as f:
            response_content = f.read()
        mock = MockRequests(response_content=response_content)
        monkeypatch.setattr(requests, "get", mock.get)
        customer = self.api.customers.get_by_id(30930235)

        with open("tests/responses/customers/modify_customer.txt", "rb") as f:
            response_content = f.read()
        mock = MockRequests(response_content=response_content)
        monkeypatch.setattr(requests, "post", mock.post)

        customer.name = "Updated Name"
        result = self.api.customers.modify(customer)

        assert result is True

    def test_generate_token(self, monkeypatch):
        """Test generate token"""
        with open("tests/responses/customers/generate_token.txt", "rb") as f:
            response_content = f.read()
        mock = MockRequests(response_content=response_content)
        monkeypatch.setattr(requests, "get", mock.get)

        token = self.api.customers.generate_token(
            username="email@email.com", password="password9", ip_address="127.0.0.1"
        )

        assert isinstance(token, str)
        assert uuid.UUID(token).version == 4

    def test_generate_login_token(self, monkeypatch):
        """Test generate login token"""
        with open("tests/responses/customers/generate_login_token.txt", "rb") as f:
            response_content = f.read()
        mock = MockRequests(response_content=response_content)
        monkeypatch.setattr(requests, "get", mock.get)

        token = self.api.customers.generate_login_token(
            customer_id=30930235, ip_address="127.0.0.1"
        )

        assert isinstance(token, str)
        assert uuid.UUID(token).version == 4

    def test_authenticate_token(self, monkeypatch):
        """Test authenticate token"""
        with open("tests/responses/customers/authenticate_token.txt", "rb") as f:
            response_content = f.read()
        mock = MockRequests(response_content=response_content)
        monkeypatch.setattr(requests, "get", mock.get)

        result = self.api.customers.authenticate_token(
            token="89c4109f-ab08-4065-bf7f-8c41c2b1f34a"
        )

        assert isinstance(result, customer_models.Customer)
        assert isinstance(result.address, customer_models.Address)

    def test_change_password(self, monkeypatch):
        """Test change password"""
        with open("tests/responses/customers/change_password.txt", "rb") as f:
            response_content = f.read()
        mock = MockRequests(response_content=response_content)
        monkeypatch.setattr(requests, "post", mock.post)

        result = self.api.customers.change_password(
            customer_id=30930235, new_password="password9"
        )

        assert result is True

    def test_forgot_password(self, monkeypatch):
        """Test forgot password"""
        with open("tests/responses/customers/forgot_password.txt", "rb") as f:
            response_content = f.read()
        mock = MockRequests(response_content=response_content)
        monkeypatch.setattr(requests, "get", mock.get)

        result = self.api.customers.forgot_password(username="email@email.com")

        assert result is True

    def test_delete_customer(self, monkeypatch):
        """Test delete customer"""
        with open("tests/responses/customers/delete_customer.txt", "rb") as f:
            response_content = f.read()
        mock = MockRequests(response_content=response_content)
        monkeypatch.setattr(requests, "post", mock.post)

        result = self.api.customers.delete(customer_id=31068890)

        assert result is True
