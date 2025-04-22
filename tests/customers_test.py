"""Customers Unit Tests"""

import pytest
import requests


class MockResponse:
    @staticmethod
    def get(*args, **kwargs):
        """Get mock response from API"""
        r = requests.Response()
        r.encoding = "UTF-8"
        r.status_code = 200
        with open("tests/responses/customers.txt", "rb") as f:
            r._content = f.read()
        return r


@pytest.mark.usefixtures("api_class")
class TestSearchCustomers:
    """Test SearchCustomers"""

    def test_search_first_ten_customers(self, monkeypatch):
        """Test search first ten customers"""
        mock = MockResponse()
        monkeypatch.setattr(requests, "get", mock.get)

        customers = self.api.customers.search(10, 1)
        assert 10 >= len(customers)
