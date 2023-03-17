"""Domains URL endpoints"""


from .base import BaseURLs


class DomainsURLs(BaseURLs):
    """Stores all API URLs to search, register or renew domain names"""

    base_url = "domains/"

    def check_availability(self):
        """Domain availability check URL"""
        return f"{self.base_url}available.json"

    def check_idn_availability(self):
        """Internationalized Domain Name availability check URL"""
        return f"{self.base_url}idn-available.json"

    def check_premium_availability(self):
        """Premium domain availability check URL"""
        return f"{self.base_url}premium/available.json"

    def check_third_level_name_availability(self):
        """3rd level .NAME availability check URL"""
        return f"{self.base_url}thirdlevelname/available.json"

    def suggest_names(self):
        """Suggest Names URL"""
        return f"{self.base_url}v5/suggest-names.json"
