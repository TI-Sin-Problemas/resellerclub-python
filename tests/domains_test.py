"""Unit Tests"""
import unittest

import idna
import tests_settings as settings

from src.resellerclub import ResellerClubAPI
from src.resellerclub.client.domains import Availability, Suggestion


class ResellerClubAPITestCase(unittest.TestCase):
    """Base ResellerClub API Test Case"""

    api = ResellerClubAPI(settings.RESELLER_ID, settings.API_KEY)


class TestDomainAvailability(ResellerClubAPITestCase):
    """Domain Availability Test Cases"""

    domains = ["github", "google"]
    tlds = ["com", "net"]

    def test_single_domain_single_tld(self):
        """Test single domain with single TLD case"""
        domain = self.domains[0]
        tld = self.tlds[0]
        result = self.api.domains.check_availability([domain], [tld])

        expected_domain = f"{domain}.{tld}"
        self.assertIn(expected_domain, result.keys())
        self.assertIsInstance(result[expected_domain], Availability)

    def test_single_domain_multiple_tlds(self):
        """Test single domain with multiple TLDs case"""
        domain = self.domains[0]
        tlds = self.tlds
        result = self.api.domains.check_availability([domain], tlds)

        expected_domains = [f"{domain}.{tld}" for tld in tlds]
        self.assertListEqual(sorted(expected_domains), sorted(list(result.keys())))
        self.assertTrue(all(isinstance(v, Availability) for v in result.values()))

    def test_multiple_domains_single_tld(self):
        """Test multiple domains with single TLD case"""
        domains = self.domains
        tld = self.tlds[0]
        result = self.api.domains.check_availability(domains, [tld])

        expected_domains = [f"{domain}.{tld}" for domain in domains]
        self.assertListEqual(sorted(expected_domains), sorted(list(result.keys())))
        self.assertTrue(all(isinstance(v, Availability) for v in result.values()))

    def test_multiple_domains_multiple_tlds(self):
        """Test multiple domains with multiple TLDs case"""
        domains = self.domains
        tlds = self.tlds
        result = self.api.domains.check_availability(domains, tlds)

        expected_domains = [f"{domain}.{tld}" for domain in domains for tld in tlds]
        self.assertListEqual(sorted(expected_domains), sorted(list(result.keys())))
        self.assertTrue(all(isinstance(v, Availability) for v in result.values()))


class TestIDNAvailability(ResellerClubAPITestCase):
    """IDN Availability Test Cases"""

    domains = ["ѯҋ111", "ѯҋ112"]
    tld = "com"
    idn_language_code = "aze"

    def test_single_domain(self):
        """Test single IDN case"""
        domain = self.domains[0]
        tld = self.tld
        result = self.api.domains.check_idn_availability(
            [domain], tld, self.idn_language_code
        )

        punycode_domain = idna.encode(domain).decode()
        expected_domain = f"{punycode_domain}.{tld}"
        self.assertIn(expected_domain, result.keys())
        self.assertIsInstance(result[expected_domain], Availability)

    def test_multiple_domains(self):
        """Test multiple IDNs case"""
        domains = self.domains
        tld = self.tld
        result = self.api.domains.check_idn_availability(
            domains, tld, self.idn_language_code
        )

        punycode_domains = [idna.encode(domain).decode() for domain in domains]
        expected_domains = [f"{domain}.{tld}" for domain in punycode_domains]
        self.assertListEqual(sorted(expected_domains), sorted(result.keys()))
        self.assertTrue(all(isinstance(v, Availability) for v in result.values()))


class TestPremiumDomainsAvailability(ResellerClubAPITestCase):
    """Premium domains availability check test case"""

    keyword = "domain"
    tlds = ["com", "net", "org"]
    highest_price = 10000
    lowest_price = 100
    max_results = 10

    def test_single_tld(self):
        """Test single TLD case"""
        keyword = self.keyword
        tld = self.tlds[0]

        response = self.api.domains.check_premium_domain_availability(keyword, [tld])

        domains = response.keys()
        is_keyword_in_domains = all(keyword in domain for domain in domains)
        is_tld_in_domains = all(domain.endswith(tld) for domain in domains)

        self.assertTrue(is_keyword_in_domains, "Keyword is not in response")
        self.assertTrue(is_tld_in_domains, "TLD is not in response")

    def test_multiple_tlds(self):
        """Test multiple TLDs case"""
        keyword = self.keyword
        tlds = self.tlds

        response = self.api.domains.check_premium_domain_availability(keyword, tlds)

        domains = response.keys()
        is_keyword_in_domains = all(keyword in key for key in response)
        is_tld_in_domains = all(any(d.endswith(tld) for d in domains) for tld in tlds)

        self.assertTrue(is_keyword_in_domains, "Keyword is not in response")
        self.assertTrue(is_tld_in_domains, "TLD is not in response")

    def test_highest_price(self):
        """Test highest price case"""
        highest_price = self.highest_price
        params = [self.keyword, self.tlds[0], highest_price]
        response = self.api.domains.check_premium_domain_availability(*params)

        self.assertGreaterEqual(highest_price, max(response.values()))

    def test_lowest_price(self):
        """Test lowest price case"""
        lowest_price = self.lowest_price
        params = [self.keyword, self.tlds[0], None, lowest_price]
        response = self.api.domains.check_premium_domain_availability(*params)

        self.assertGreaterEqual(min(response.values()), lowest_price)

    def test_highest_and_lowest_price(self):
        """Test highest and lowest price case"""
        lowest_price = self.lowest_price
        highest_price = self.highest_price
        params = [self.keyword, self.tlds[0], highest_price, lowest_price]
        response = self.api.domains.check_premium_domain_availability(*params)

        prices = response.values()
        self.assertGreaterEqual(min(prices), lowest_price)
        self.assertGreaterEqual(highest_price, max(prices))

    def test_max_results(self):
        """Test max results case"""
        max_results = self.max_results
        params = {
            "keyword": self.keyword,
            "tlds": self.tlds[0],
            "max_results": max_results,
        }
        response = self.api.domains.check_premium_domain_availability(**params)

        self.assertGreaterEqual(max_results, len(response))


class TestThirdLvlNameAvailability(ResellerClubAPITestCase):
    """.NAME 3rd level availability check test case"""

    domains = ["domain.one", "domain.two"]

    def test_single_domain(self):
        """Test single domain case"""
        result = self.api.domains.check_third_level_name_availability(self.domains[0])

        expected_domain = f"{self.domains[0]}.name"
        self.assertListEqual([expected_domain], list(result.keys()))
        self.assertIsInstance(result[expected_domain], Availability)

    def test_multiple_domain(self):
        """Test multiple domain case"""
        result = self.api.domains.check_third_level_name_availability(self.domains)

        expected_domains = [f"{domain}.name" for domain in self.domains]
        self.assertListEqual(sorted(expected_domains), sorted(result.keys()))
        self.assertTrue(all(isinstance(v, Availability) for v in result.values()))


class TestSuggestNames(ResellerClubAPITestCase):
    """Suggest name test case"""

    keyword = "reseller"

    def test_keyword_only(self):
        """Test suggest names with keyword only"""
        suggestions = self.api.domains.suggest_names(self.keyword)
        self.assertTrue(all(isinstance(sug, Suggestion) for sug in suggestions))

    def test_tld(self):
        """Test suggest names with keyword and .com tld"""
        tld = "com"
        suggestions = self.api.domains.suggest_names(self.keyword, tld)
        assertion = all(s.domain.endswith(f".{tld}") for s in suggestions)
        self.assertTrue(assertion, "Some results do not contain TLD")

    def test_exact_match(self):
        """Test suggest names with keyword exact match"""
        suggestions = self.api.domains.suggest_names(self.keyword, exact_match=True)
        assertion = all(s.domain.split(".")[0] == self.keyword for s in suggestions)
        self.assertTrue(assertion, "Results are not exact match")
