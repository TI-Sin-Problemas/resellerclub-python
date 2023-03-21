"""Tests settings"""
import os

from dotenv import load_dotenv

load_dotenv()


RESELLER_ID = os.getenv("RESELLERCLUB_RESELLER_ID")
API_KEY = os.getenv("RESELLERCLUB_API_KEY")
