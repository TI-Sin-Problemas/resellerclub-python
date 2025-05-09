"""Customers Unit Tests"""

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

    def get(self, *args, **kwargs):
        """Get mock response from API"""
        return self.response

    def post(self, *args, **kwargs):
        return self.response


@pytest.mark.usefixtures("api_class")
class TestSearchCustomers:
    """Test SearchCustomers"""

    api: ResellerClub

    def test_sign_up_customer(self, monkeypatch):
        """Test sign up a new customer"""
        with open("tests/responses/sign_up.txt", "rb") as f:
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
        with open("tests/responses/customers.txt", "rb") as f:
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
        with open("tests/responses/customer_details.txt", "rb") as f:
            response_content = f.read()
        mock = MockRequests(response_content=response_content)
        monkeypatch.setattr(requests, "get", mock.get)

        customer = self.api.customers.get_by_username("email@email.com")
        assert isinstance(customer, customer_models.Customer)
        assert isinstance(customer.address, customer_models.Address)
        assert isinstance(customer.phones, customer_models.CustomerPhones)

    def test_get_customer_by_id(self, monkeypatch):
        """Test get customer by ID"""
        with open("tests/responses/customer_details.txt", "rb") as f:
            response_content = f.read()
        mock = MockRequests(response_content=response_content)
        monkeypatch.setattr(requests, "get", mock.get)

        customer = self.api.customers.get_by_id(30930235)
        assert isinstance(customer, customer_models.Customer)
        assert isinstance(customer.address, customer_models.Address)
