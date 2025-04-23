"""Customers API Client"""

from datetime import datetime
from typing import Iterator, List, Literal, NamedTuple

from .base import BaseClient


class Customer(NamedTuple):
    """Customer object"""

    id: str
    username: str
    reseller_id: str
    name: str
    company: str
    city: str
    state: str
    country: str
    status: str
    total_receipts: float
    phone: str
    phone_country_code: str
    website_count: int


class SearchResponse(NamedTuple):
    """Represents the result of a customer search"""

    page_records: int
    db_records: int
    customers: List[Customer]

    def __len__(self) -> int:
        return len(self.customers)

    def __iter__(self) -> Iterator:
        return self.customers.__iter__()


class CustomersClient(BaseClient):
    """Customers API Client"""

    def sign_up(
        self,
        username: str,
        password: str,
        name: str,
        company: str,
        address: str,
        city: str,
        state: str,
        country: str,
        zip_code: str,
        phone_country_code: str,
        phone: str,
        language_code: str,
        other_state: str = None,
        address2: str = None,
        address3: str = None,
        alt_phone_country_code: str = None,
        alt_phone: str = None,
        mobile_country_code: str = None,
        mobile: str = None,
        sms_consent: bool = None,
        vat_number: str = None,
        accept_policy: str = None,
        marketing_consent: bool = None,
    ) -> int:
        """
        Registers a new customer.

        For more details see: https://manage.resellerclub.com/kb/answer/804

        Args:
            username (str): Username for the Customer Account. Username should be an email address.
            password (str): Password for the Customer Account.
            name (str): Name of the Customer
            company (str): Name of the Customer's company
            address (str): Address line 1 of the Customer's address
            city (str): City.
            state (str): State. In case the State information is not available, you need to pass
                the value for this parameter as Not Applicable.
            country (str): Country Code as per ISO 3166-1 alpha-2
            zip_code (str): ZIP code
            phone_country_code (str): Telephone number Country Code
            phone (str): Phone number
            language_code (str): Language Code as per ISO
            other_state (str, optional): This parameter needs to be included if the State
                information is not available. Mention an appropriate value for this
                parameter.
            address2 (str, optional): Address line 2 of the Customer's address
            address3 (str, optional): Address line 3 of the Customer's address
            alt_phone_country_code (str, optional): Alternate phone country code
            alt_phone (str, optional): Alternate phone number
            mobile_country_code (str, optional): Mobile country code
            mobile (str, optional): Mobile number
            sms_consent (bool, optional): In case of a US based customer, consent is required to
                receive renewal reminder SMSes
            vat_number (str, optional): VAT ID for EU VAT
            accept_policy (str, optional): Accept Terms and Conditions and Privacy Policy to create
                an account
            marketing_consent (bool, optional): In case of EEA (European Economic Area) countries
                capture consent to receive marketing emails

        Returns:
            int: The new customer ID.
        """
        url = self._urls.customers.signup
        params = {
            "username": username,
            "passwd": password,
            "name": name,
            "company": company,
            "address-line-1": address,
            "city": city,
            "state": state,
            "other-state": other_state,
            "country": country,
            "zipcode": zip_code,
            "phone-cc": phone_country_code,
            "phone": phone,
            "lang-pref": language_code,
            "address-line-2": address2,
            "address-line-3": address3,
            "alt-phone-cc": alt_phone_country_code,
            "alt-phone": alt_phone,
            "mobile-cc": mobile_country_code,
            "mobile": mobile,
            "sms-consent": sms_consent,
            "vat-id": vat_number,
            "accept-policy": accept_policy,
            "marketing-email-consent": marketing_consent,
        }
        return self._post(url, params)

    def search(
        self,
        records: int,
        page: int,
        customers: List[str] | str = None,
        resellers: List[str] | str = None,
        username: str = None,
        name: str = None,
        company: str = None,
        city: str = None,
        state: str = None,
        status: Literal["Active", "Suspended", "Deleted"] = None,
        creation_date_start: datetime = None,
        creation_date_end: datetime = None,
        total_receipt_start: float = None,
        total_receipt_end: float = None,
    ) -> SearchResponse[Customer]:
        """Gets details of the Customers that match the search criteria

        Args:
            records (int): Number of records to be fetched.
            page (int): Page number for which details are to be fetched
            customers (List[str] | str, optional): Customer ID(s). Defaults to None.
            resellers (List[str] | str, optional): Reseller ID(s) for whom Customer accounts need
            to be searched. Defaults to None.
            username (str, optional): Username of Customer. Should be an email address.
            Defaults to None.
            name (str, optional): Name of Customer. Defaults to None.
            company (str, optional): Comany name of Customer. Defaults to None.
            city (str, optional): City. Defaults to None.
            state (str, optional): State. Defaults to None.
            status (Literal["Active", "Suspended", "Deleted"], optional): Status of Customer.
            Defaults to None.
            creation_date_start (datetime, optional): DateTime for listing of Customer accounts
            whose Creation Date is greater than. Defaults to None.
            creation_date_end (datetime, optional): DateTime for listing of Customer accounts whose
            Creation Date is less than. Defaults to None.
            total_receipt_start (float, optional): Total receipts of Customer which is greater than.
            Defaults to None.
            total_receipt_end (float, optional): Total receipts of Customer which is less than.
            Defaults to None.

        Returns:
            SearchResponse[Customer]: Object containing Customer objects for each client matching
            search criteria
        """

        if isinstance(customers, str):
            customers = [customers]
        if isinstance(resellers, str):
            resellers = [resellers]
        if creation_date_start:
            creation_date_start = creation_date_start.timestamp()
        if creation_date_end:
            creation_date_end = creation_date_end.timestamp()

        url = self._urls.customers.search
        params = {
            "no-of-records": records,
            "page-no": page,
            "customer-id": customers,
            "reseller-id": resellers,
            "username": username,
            "name": name,
            "company": company,
            "city": city,
            "state": state,
            "status": status,
            "creation-date-start": creation_date_start,
            "creation-date-end": creation_date_end,
            "total-receipt-start": total_receipt_start,
            "total-receipt-end": total_receipt_end,
        }
        data = self._get(url, params)

        recsonpage = int(data.get("recsonpage"))
        recsindb = int(data.get("recsindb"))
        customers = []
        for key, value in data.items():
            if key.isdigit():
                customer_data = {k.split(".")[1]: v for k, v in value.items()}
                customer_params = {
                    "id": customer_data["customerid"],
                    "username": customer_data["username"],
                    "reseller_id": customer_data["resellerid"],
                    "name": customer_data["name"],
                    "company": customer_data["company"],
                    "city": customer_data["city"],
                    "state": customer_data.get("state"),
                    "country": customer_data["country"],
                    "status": customer_data["customerstatus"],
                    "total_receipts": float(customer_data["totalreceipts"]),
                    "phone": customer_data["telno"],
                    "phone_country_code": customer_data["telnocc"],
                    "website_count": int(customer_data["websitecount"]),
                }
                customers.append(Customer(**customer_params))

        return SearchResponse(recsonpage, recsindb, customers)
