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


class TestPremiumDomainsAvailability(ResellerClubAPITestCase):
    """Premium domains availability check test case"""

    keyword = "domain"
    single_tld = ["com"]
    multiple_tlds = ["com", "net", "org"]
    highest_price = 10000
    lowest_price = 100
    max_results = 10

    def test_single_tld(self):
        """Test single TLD case"""
        keyword = self.keyword
        tlds = self.single_tld

        response = self.api.check_premium_domain_availability(keyword, tlds)

        keyword_in_response = all(keyword in key for key in response)

        tld_in_response = False
        for tld in tlds:
            tld_in_response = all(tld in key for key in response)
            if tld_in_response is False:
                break

        self.assertTrue(keyword_in_response, "Keyword is not in response")
        self.assertTrue(tld_in_response, "TLD is not in response")

    def test_multiple_tlds(self):
        """Test multiple TLDs case"""
        keyword = self.keyword
        tlds = self.multiple_tlds

        response = self.api.check_premium_domain_availability(keyword, tlds)

        keyword_in_response = all(keyword in key for key in response)

        tld_in_response = False
        for tld in tlds:
            tld_in_response = any(tld in key for key in response)
            if tld_in_response is False:
                break

        self.assertTrue(keyword_in_response, "Keyword is not in response")
        self.assertTrue(tld_in_response, "TLD is not in response")

    def test_highest_price(self):
        """Test highest price case"""
        highest_price = self.highest_price

        response = self.api.check_premium_domain_availability(
            self.keyword, self.single_tld, highest_price
        )

        response_highest_price = 0
        prices = [float(item[1]) for item in response.items()]
        response_highest_price = max(prices)

        self.assertGreaterEqual(highest_price, response_highest_price)

    def test_lowest_price(self):
        """Test lowest price case"""
        lowest_price = self.lowest_price

        response = self.api.check_premium_domain_availability(
            self.keyword, self.single_tld, lowest_price=lowest_price
        )

        prices = [float(item[1]) for item in response.items()]
        response_lowest_price = min(prices)

        self.assertGreaterEqual(response_lowest_price, lowest_price)

    def test_highest_and_lowest_price(self):
        """Test highest and lowest price case"""
        lowest_price = self.lowest_price
        highest_price = self.highest_price

        response = self.api.check_premium_domain_availability(
            self.keyword, self.single_tld, highest_price, lowest_price
        )

        prices = [float(item[1]) for item in response.items()]
        response_lowest_price = min(prices)
        response_highest_price = max(prices)

        self.assertGreaterEqual(response_lowest_price, lowest_price)
        self.assertGreaterEqual(highest_price, response_highest_price)

    def test_max_results(self):
        """Test max results case"""

        max_results = self.max_results

        response = self.api.check_premium_domain_availability(
            self.keyword, self.single_tld, max_results=max_results
        )

        self.assertGreaterEqual(max_results, len(response))


class TestThirdLvlNameAvailability(ResellerClubAPITestCase):
    """.NAME 3rd level availability check test case"""

    def test_single_domain(self):
        """Test single domain case"""
        domain_names = ["domain.one"]
        response = self.api.check_third_level_name_availability(domain_names)
        test_against = {
            "domain.one.name": {"classkey": "dotname", "status": "available"}
        }

        self.assertDictContainsSubset(response, test_against)

    def test_multiple_domain(self):
        """Test multiple domain case"""
        domain_names = ["domain.one", "domain.two"]
        response = self.api.check_third_level_name_availability(domain_names)
        test_against = {
            "domain.two.name": {"classkey": "dotname", "status": "available"},
            "domain.one.name": {"classkey": "dotname", "status": "available"},
        }

        self.assertDictContainsSubset(response, test_against)
