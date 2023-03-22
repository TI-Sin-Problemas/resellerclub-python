"""Customers Unit Tests"""
from case import ResellerClubTestCase


class TestSearchCustomers(ResellerClubTestCase):
    """Test SearchCustomers"""

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.search_method = self.api.customers.search

    def test_search_first_ten_customers(self):
        """Test search first ten customers"""
        customers = self.search_method(10, 1)
        self.assertGreaterEqual(10, len(customers))
