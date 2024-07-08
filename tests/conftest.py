"""Tests settings"""

import os

import pytest

from src.resellerclub import ResellerClub

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

RESELLER_ID = os.getenv("RESELLERCLUB_RESELLER_ID")
API_KEY = os.getenv("RESELLERCLUB_API_KEY")


@pytest.fixture(scope="class")
def api_class(request):
    """Fixture to set up the ResellerClub API for the test class."""
    request.cls.api = ResellerClub(RESELLER_ID, API_KEY)
