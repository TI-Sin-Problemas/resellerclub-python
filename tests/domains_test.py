"""Domains Unit Tests"""

from unittest import TestCase

import idna
import pytest
import requests
from thefuzz import fuzz

from src.resellerclub import ResellerClub
from src.resellerclub.models import domains as domain_models

from .mocks import MockRequests


@pytest.mark.usefixtures("api_class")
class TestDomainAvailability:
    """Domain Availability Test Cases"""

    api: ResellerClub

    domains = ["github", "google"]
    tlds = ["com", "net"]

    def test_single_domain_single_tld(self, monkeypatch):
        """Test single domain with single TLD case"""
        with open(
            "tests/responses/domains/availability/single_domain_availability.txt", "rb"
        ) as f:
            content = f.read()
        mock = MockRequests(response_content=content)
        monkeypatch.setattr(requests, "get", mock.get)

        domain = self.domains[0]
        tld = self.tlds[0]
        result = self.api.domains.check_availability([domain], [tld])

        assert all(isinstance(a, domain_models.Availability) for a in result)

    def test_single_domain_multiple_tlds(self, monkeypatch):
        """Test single domain with multiple TLDs case"""
        with open(
            "tests/responses/domains/availability/single_domain_multiple_tlds.txt", "rb"
        ) as f:
            content = f.read()
        mock = MockRequests(response_content=content)
        monkeypatch.setattr(requests, "get", mock.get)

        domain = self.domains[0]
        tlds = self.tlds
        result = self.api.domains.check_availability([domain], tlds)

        assert all(isinstance(a, domain_models.Availability) for a in result)

        expected_domains = [f"{domain}.{tld}" for tld in tlds]
        result_domains = [a.domain for a in result]
        assert sorted(expected_domains) == sorted(result_domains)

    def test_multiple_domains_single_tld(self, monkeypatch):
        """Test multiple domains with single TLD case"""
        with open(
            "tests/responses/domains/availability/multiple_domains_single_tld.txt", "rb"
        ) as f:
            content = f.read()
        mock = MockRequests(response_content=content)
        monkeypatch.setattr(requests, "get", mock.get)

        domains = self.domains
        tld = self.tlds[0]
        result = self.api.domains.check_availability(domains, [tld])

        assert all(isinstance(a, domain_models.Availability) for a in result)

        expected_domains = [f"{domain}.{tld}" for domain in domains]
        result_domains = [a.domain for a in result]
        assert sorted(expected_domains) == sorted(result_domains)

    def test_multiple_domains_multiple_tlds(self, monkeypatch):
        """Test multiple domains with multiple TLDs case"""
        with open(
            "tests/responses/domains/availability/multiple_domains_multiple_tlds.txt",
            "rb",
        ) as f:
            content = f.read()
        mock = MockRequests(response_content=content)
        monkeypatch.setattr(requests, "get", mock.get)

        domains = self.domains
        tlds = self.tlds
        result = self.api.domains.check_availability(domains, tlds)

        assert all(isinstance(a, domain_models.Availability) for a in result)

        expected_domains = [f"{domain}.{tld}" for domain in domains for tld in tlds]
        result_domains = [a.domain for a in result]
        assert sorted(expected_domains) == sorted(result_domains)


@pytest.mark.usefixtures("api_class")
class TestIDNAvailability:
    """IDN Availability Test Cases"""

    api: ResellerClub

    domains = ["ѯҋ111", "ѯҋ112"]
    tld = "com"
    idn_language_code = "aze"
    responses_dir = "tests/responses/domains/idn_availability"

    def test_single_domain(self, monkeypatch):
        """Test single IDN case"""
        with open(f"{self.responses_dir}/single_domain.txt", "rb") as f:
            content = f.read()
        mock = MockRequests(response_content=content)
        monkeypatch.setattr(requests, "get", mock.get)

        domain = self.domains[0]
        tld = self.tld
        result = self.api.domains.check_idn_availability(
            [domain], tld, self.idn_language_code
        )

        assert all(isinstance(a, domain_models.Availability) for a in result)

        punycode_domain = idna.encode(domain).decode()
        expected_domain = f"{punycode_domain}.{tld}"
        assert expected_domain in [a.domain for a in result]

    def test_multiple_domains(self, monkeypatch):
        """Test multiple IDNs case"""
        with open(f"{self.responses_dir}/multiple_domains.txt", "rb") as f:
            content = f.read()
        mock = MockRequests(response_content=content)
        monkeypatch.setattr(requests, "get", mock.get)

        domains = self.domains
        tld = self.tld
        result = self.api.domains.check_idn_availability(
            domains, tld, self.idn_language_code
        )

        assert all(isinstance(a, domain_models.Availability) for a in result)

        punycode_domains = [idna.encode(domain).decode() for domain in domains]
        expected_domains = [f"{domain}.{tld}" for domain in punycode_domains]
        result_domains = [a.domain for a in result]
        assert sorted(expected_domains) == sorted(result_domains)


@pytest.mark.usefixtures("api_class")
class TestPremiumDomainsAvailability:
    """Premium domains availability check test case"""

    api: ResellerClub

    keyword = "domain"
    tlds = ["com", "net", "org"]
    highest_price = 10000
    lowest_price = 100
    max_results = 10
    responses_dir = "tests/responses/domains/premium_domain_availability"

    def test_single_tld(self, monkeypatch):
        """Test single TLD case"""
        with open(f"{self.responses_dir}/single_tld.txt", "rb") as f:
            content = f.read()
        mock = MockRequests(response_content=content)
        monkeypatch.setattr(requests, "get", mock.get)

        keyword = self.keyword
        tld = self.tlds[0]

        response = self.api.domains.check_premium_domain_availability(keyword, [tld])

        assert all(isinstance(pd, domain_models.PremiumDomain) for pd in response)

        domains = [pd.domain for pd in response]
        is_keyword_in_domains = all(keyword in domain for domain in domains)
        is_tld_in_domains = all(domain.endswith(f".{tld}") for domain in domains)

        assert is_keyword_in_domains is True, "Keyword is not in response"
        assert is_tld_in_domains is True, "TLD is not in response"

    def test_multiple_tlds(self, monkeypatch):
        """Test multiple TLDs case"""
        with open(f"{self.responses_dir}/multiple_tlds.txt", "rb") as f:
            content = f.read()
        mock = MockRequests(response_content=content)
        monkeypatch.setattr(requests, "get", mock.get)

        keyword = self.keyword
        tlds = self.tlds

        response = self.api.domains.check_premium_domain_availability(keyword, tlds)

        assert all(isinstance(pd, domain_models.PremiumDomain) for pd in response)

        domains = [pd.domain for pd in response]
        is_keyword_in_domains = all(keyword in key for key in domains)
        is_tld_in_domains = all(any(d.endswith(f".{t}") for d in domains) for t in tlds)

        assert is_keyword_in_domains is True, "Keyword is not in response"
        assert is_tld_in_domains is True, "TLD is not in response"

    def test_highest_price(self, monkeypatch):
        """Test highest price case"""
        with open(f"{self.responses_dir}/highest_price.txt", "rb") as f:
            content = f.read()
        mock = MockRequests(response_content=content)
        monkeypatch.setattr(requests, "get", mock.get)

        highest_price = self.highest_price
        params = [self.keyword, self.tlds[0], highest_price]
        response = self.api.domains.check_premium_domain_availability(*params)
        prices = [pd.price for pd in response]

        assert highest_price >= max(prices)

    def test_lowest_price(self, monkeypatch):
        """Test lowest price case"""
        with open(f"{self.responses_dir}/highest_price.txt", "rb") as f:
            content = f.read()
        mock = MockRequests(response_content=content)
        monkeypatch.setattr(requests, "get", mock.get)

        lowest_price = self.lowest_price
        params = [self.keyword, self.tlds[0], None, lowest_price]
        response = self.api.domains.check_premium_domain_availability(*params)
        prices = [pd.price for pd in response]

        assert lowest_price <= min(prices)

    def test_highest_and_lowest_price(self, monkeypatch):
        """Test highest and lowest price case"""
        with open(f"{self.responses_dir}/highest_and_lowest_price.txt", "rb") as f:
            content = f.read()
        mock = MockRequests(response_content=content)
        monkeypatch.setattr(requests, "get", mock.get)

        lowest_price = self.lowest_price
        highest_price = self.highest_price
        params = [self.keyword, self.tlds[0], highest_price, lowest_price]
        response = self.api.domains.check_premium_domain_availability(*params)
        prices = [pd.price for pd in response]

        assert lowest_price <= min(prices)
        assert highest_price >= max(prices)

    def test_max_results(self, monkeypatch):
        """Test max results case"""
        with open(f"{self.responses_dir}/max_results.txt", "rb") as f:
            content = f.read()
        mock = MockRequests(response_content=content)
        monkeypatch.setattr(requests, "get", mock.get)

        max_results = self.max_results
        params = {
            "keyword": self.keyword,
            "tlds": self.tlds[0],
            "max_results": max_results,
        }
        response = self.api.domains.check_premium_domain_availability(**params)

        assert max_results >= len(response)


@pytest.mark.usefixtures("api_class")
class TestThirdLvlNameAvailability:
    """.NAME 3rd level availability check test case"""

    api: ResellerClub

    domains = ["domain.one", "domain.two"]
    responses_dir = "tests/responses/domains/3rd_level_name_availability"

    def test_single_domain(self, monkeypatch):
        """Test single domain case"""
        with open(f"{self.responses_dir}/single_domain.txt", "rb") as f:
            content = f.read()
        mock = MockRequests(response_content=content)
        monkeypatch.setattr(requests, "get", mock.get)

        result = self.api.domains.check_third_level_name_availability(self.domains[0])

        expected_domain = f"{self.domains[0]}.name"
        result_domains = [a.domain for a in result]

        assert all(isinstance(a, domain_models.Availability) for a in result)
        assert [expected_domain] == result_domains

    def test_multiple_domains(self, monkeypatch):
        """Test multiple domain case"""
        with open(f"{self.responses_dir}/multiple_domains.txt", "rb") as f:
            content = f.read()
        mock = MockRequests(response_content=content)
        monkeypatch.setattr(requests, "get", mock.get)

        result = self.api.domains.check_third_level_name_availability(self.domains)

        expected_domains = [f"{domain}.name" for domain in self.domains]
        result_domains = [a.domain for a in result]

        assert all(isinstance(a, domain_models.Availability) for a in result)
        assert sorted(expected_domains) == sorted(result_domains)


@pytest.mark.usefixtures("api_class")
class TestSuggestNames:
    """Suggest name test case"""

    api: ResellerClub

    keyword = "reseller"
    responses_dir = "tests/responses/domains/suggest_names"

    def test_keyword_only(self, monkeypatch):
        """Test suggest names with keyword only"""
        with open(f"{self.responses_dir}/keyword_only.txt", "rb") as f:
            content = f.read()
        mock = MockRequests(response_content=content)
        monkeypatch.setattr(requests, "get", mock.get)

        suggestions = self.api.domains.suggest_names(self.keyword)

        assert all(isinstance(s, domain_models.Suggestion) for s in suggestions)

        ratio_list = [fuzz.partial_ratio(s.domain, self.keyword) for s in suggestions]
        failed_message = "Some results are less than 75% similar"
        assert any(ratio < 75 for ratio in ratio_list) is False, failed_message

    def test_tld(self, monkeypatch):
        """Test suggest names with keyword and .com tld"""
        with open(f"{self.responses_dir}/tld.txt", "rb") as f:
            content = f.read()
        mock = MockRequests(response_content=content)
        monkeypatch.setattr(requests, "get", mock.get)

        tld = "com"
        suggestions = self.api.domains.suggest_names(self.keyword, tld)

        assert all(isinstance(s, domain_models.Suggestion) for s in suggestions)

        assertion = all(s.domain.endswith(f".{tld}") for s in suggestions)
        assert assertion is True, "Some results do not contain TLD"

    def test_exact_match(self):
        """Test suggest names with keyword exact match"""
        suggestions = self.api.domains.suggest_names(self.keyword, exact_match=True)
        assertion = all(s.domain.split(".")[0] == self.keyword for s in suggestions)
        self.assertTrue(assertion, "Results are not exact match")
