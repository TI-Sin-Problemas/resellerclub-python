"""Reseller Club API Test Case"""
from unittest import TestCase

from settings import API_KEY, RESELLER_ID

from src.resellerclub import ResellerClub


class ResellerClubTestCase(TestCase):
    """Base ResellerClub API Test Case"""

    api = ResellerClub(RESELLER_ID, API_KEY)
