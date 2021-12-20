"""Unit Tests"""
import unittest
import tests_settings as settings

from resellerclub import ResellerClubAPI


class ResellerClubAPITestCase(unittest.TestCase):
    """Base ResellerClub API Test Case"""

    api = ResellerClubAPI(settings.RESELLER_ID, settings.API_KEY)


class TestDomainAvailability(ResellerClubAPITestCase):
    """Domain Availability Test Cases"""

    single_domain = ["github"]
    single_tld = ["com"]
    multiple_domains = ["github", "google"]
    multiple_tlds = ["com", "net"]

    def test_single_domain_single_tld(self):
        """Test single domain with single TLD case"""
        domain_names = self.single_domain
        tlds = self.single_tld
        test_against = {
            "github.com": {"classkey": "domcno", "status": "regthroughothers"}
        }
        result = self.api.check_domain_availability(domain_names, tlds)

        self.assertDictContainsSubset(result, test_against)

    def test_single_domain_multiple_tlds(self):
        """Test single domain with multiple TLDs case"""
        domain_names = self.single_domain
        tlds = self.multiple_tlds
        test_against = {
            "github.com": {"classkey": "domcno", "status": "regthroughothers"},
            "github.net": {"classkey": "dotnet", "status": "regthroughothers"},
        }
        result = self.api.check_domain_availability(domain_names, tlds)

        self.assertDictContainsSubset(result, test_against)

    def test_multiple_domains_single_tld(self):
        """Test multiple domains with single TLD case"""
        domain_names = self.multiple_domains
        tlds = self.single_tld
        test_against = {
            "github.com": {"classkey": "domcno", "status": "regthroughothers"},
            "google.com": {"classkey": "domcno", "status": "regthroughothers"},
        }
        result = self.api.check_domain_availability(domain_names, tlds)

        self.assertDictContainsSubset(result, test_against)

    def test_multiple_domains_multiple_tlds(self):
        """Test multiple domains with multiple TLDs case"""
        domain_names = self.multiple_domains
        tlds = self.multiple_tlds
        test_against = {
            "google.com": {"classkey": "domcno", "status": "regthroughothers"},
            "github.net": {"classkey": "dotnet", "status": "regthroughothers"},
            "google.net": {"classkey": "dotnet", "status": "regthroughothers"},
            "github.com": {"classkey": "domcno", "status": "regthroughothers"},
        }
        result = self.api.check_domain_availability(domain_names, tlds)

        self.assertDictContainsSubset(result, test_against)


class TestIDNAvailability(ResellerClubAPITestCase):
    """IDN Availability Test Cases"""

    single_domain = ["ѯҋ111"]
    multiple_domains = ["ѯҋ111", "ѯҋ112"]
    tld = "com"
    idn_language_code = "aze"

    def test_single_domain(self):
        """Test single IDN case"""
        domain_names = self.single_domain
        tld = self.tld
        idn_language_code = self.idn_language_code
        test_against = {
            "xn--111-dkd4l.com": {"classkey": "domcno", "status": "regthroughothers"},
        }

        result = self.api.check_domain_availability_idn(
            domain_names, tld, idn_language_code
        )

        self.assertDictContainsSubset(result, test_against)

    def test_multiple_domain(self):
        """Test multiple IDNs case"""
        domain_names = self.multiple_domains
        tld = self.tld
        idn_language_code = self.idn_language_code
        test_against = {
            "xn--111-dkd4l.com": {"classkey": "domcno", "status": "regthroughothers"},
            "xn--112-dkd4l.com": {"classkey": "domcno", "status": "regthroughothers"},
        }

        result = self.api.check_domain_availability_idn(
            domain_names, tld, idn_language_code
        )

        self.assertDictContainsSubset(result, test_against)
