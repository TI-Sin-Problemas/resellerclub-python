"""Customers Unit Tests"""

import pytest
import requests

from src.resellerclub import ResellerClub
from src.resellerclub.models import customer


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

        new_customer = customer.NewCustomer(
            username="email@email.com",
            password="password9",
            name="Customer Name",
            company="Customer Company",
            address=customer.NewCustomerAddress(
                line1="Customer Address",
                city="City",
                state="State",
                country="US",
                zip_code="12345",
            ),
            phones=customer.NewCustomerPhones(
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
        assert 10 >= len(customers)
