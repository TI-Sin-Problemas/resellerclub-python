"""Customers Unit Tests"""

import pytest
import requests


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



@pytest.mark.usefixtures("api_class")
class TestSearchCustomers:
    """Test SearchCustomers"""

    def test_search_first_ten_customers(self, monkeypatch):
        """Test search first ten customers"""
        with open("tests/responses/customers.txt", "rb") as f:
            response_content = f.read()
        mock = MockRequests(response_content=response_content)
        monkeypatch.setattr(requests, "get", mock.get)

        customers = self.api.customers.search(10, 1)
        assert 10 >= len(customers)
