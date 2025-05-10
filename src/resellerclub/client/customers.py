"""Customers API Client"""

from datetime import datetime
from typing import Iterator, List, Literal, NamedTuple

from ..models.customer import Customer, NewCustomer
from .base import BaseClient


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

    def sign_up(self, customer: NewCustomer) -> int:
        """
        Registers a new customer.

        For more details see: https://manage.resellerclub.com/kb/answer/804

        Args:
            customer (NewCustomer): Customer object with all the required details

        Returns:
            int: The new customer ID.
        """
        if customer.id is not None:
            raise ValueError("Customer ID should be None")
        url = self._urls.customers.signup
        params = {
            "username": customer.username,
            "passwd": customer.password,
            "name": customer.name,
            "company": customer.company,
            "address-line-1": customer.address.line1,
            "city": customer.address.city,
            "state": customer.address.state,
            "other-state": customer.address.other_state,
            "country": customer.address.country,
            "zipcode": customer.address.zip_code,
            "phone-cc": customer.phones.phone_country_code,
            "phone": customer.phones.phone,
            "lang-pref": customer.language_code,
            "address-line-2": customer.address.line2,
            "address-line-3": customer.address.line3,
            "alt-phone-cc": customer.phones.alt_phone_country_code,
            "alt-phone": customer.phones.alt_phone,
            "mobile-cc": customer.phones.mobile_country_code,
            "mobile": customer.phones.mobile,
            "sms-consent": customer.sms_consent,
            "vat-id": customer.vat_number,
            "accept-policy": customer.accept_policy,
            "marketing-email-consent": customer.marketing_consent,
        }
        return self._post(url, params)

    def get_by_username(self, username: str) -> Customer:
        """
        Retrieves customer details by username.

        Args:
        username (str): The username of the customer.

        Returns:
            Customer: A Customer object with the details of the specified customer.
        """

        url = self._urls.customers.details_by_username
        params = {"username": username}
        data = self._get(url, params)
        return Customer.from_details(data)

    def get_by_id(self, customer_id: int) -> Customer:
        """
        Retrieves customer details by ID.

        Args:
        customer_id (int): The ID of the customer.

        Returns:
            Customer: A Customer object with the details of the specified customer.
        """
        url = self._urls.customers.details_by_id
        params = {"customer-id": customer_id}
        data = self._get(url, params)
        return Customer.from_details(data)

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

        recsonpage = int(data.pop("recsonpage"))
        recsindb = int(data.pop("recsindb"))
        customers = []
        for value in data.values():
            customers.append(Customer.from_search(value))

        return SearchResponse(recsonpage, recsindb, customers)

    def modify(self, customer: Customer) -> bool:
        """
        Modify customer details.

        Args:
            customer (Customer): The customer object with the modified details.

        Returns:
            bool: True if the customer details are modified successfully, False otherwise.
        """
        url = self._urls.customers.modify
        if customer.id is None:
            raise ValueError("Customer ID should not be None")
        params = {
            "customer-id": customer.id,
            "username": customer.username,
            "name": customer.name,
            "company": customer.company,
            "address-line-1": customer.address.line1,
            "address-line-2": customer.address.line2,
            "city": customer.address.city,
            "state": customer.address.state,
            "other-state": customer.address.other_state,
            "country": customer.address.country,
            "zipcode": customer.address.zip_code,
            "phone-cc": customer.phones.phone_country_code,
            "phone": customer.phones.phone,
            "lang-pref": customer.language_preference,
            "address-line-3": customer.address.line3,
            "alt-phone-cc": customer.phones.alt_phone_country_code,
            "alt-phone": customer.phones.alt_phone,
            "fax-cc": customer.phones.fax_country_code,
            "fax": customer.phones.fax,
            "mobile-cc": customer.phones.mobile_country_code,
            "mobile": customer.phones.mobile,
        }
        return bool(self._post(url, params))

    def generate_token(self, username: str, password: str, ip_address: str) -> str:
        """
        Authenticates a Customer by returning an authentication token on successful authentication.
        The token will be valid for a duration of only 120 seconds.

        For more details see: https://manage.resellerclub.com/kb/answer/818

        Args:
            username (str): The username of the customer.
            password (str): The password of the customer.
            ip_address (str): The IP address of the customer.

        Returns:
            str: The generated token.
        """
        url = self._urls.customers.generate_token
        params = {
            "username": username,
            "passwd": password,
            "ip": ip_address,
        }
        return self._get(url, params)

    def generate_login_token(self, customer_id: int, ip_address: str) -> str:
        """Returns an authentication token for a Customer.

        You can login to the Customer's Control Panel using the generated token.
        The Control panel can be accessed at following link, where XXXXX is the generated token.
        `http://manage.resellerclub.com/servlet/AutoLoginServlet?userLoginId=XXXXX&role=customer`

        For more details see: https://manage.resellerclub.com/kb/answer/2942

        Args:
            customer_id (int): The ID of the customer.
            ip_address (str): The IP address of the customer.

        Returns:
            str: The generated token.
        """
        url = self._urls.customers.generate_login_token
        params = {
            "customer-id": customer_id,
            "ip": ip_address,
        }
        return self._get(url, params)

    def authenticate_token(self, token: str) -> Customer:
        """Authenticates the token generated by the `generate_token` method and returns a Customer
        object, if authenticated.

        For more details see: https://manage.resellerclub.com/kb/answer/820

        Args:
            token (str): The token to authenticate.

        Returns:
            Customer: The authenticated Customer object.
        """
        url = self._urls.customers.authenticate_token
        params = {"token": token}
        return Customer.from_auth(self._get(url, params))

    def change_password(self, customer_id: int, new_password: str) -> bool:
        """Changes the password for the specified Customer.

        For more details see: https://manage.resellerclub.com/kb/answer/806

        Args:
            customer_id (int): The Id of the Customer whose password needs to be changed.
            new_password (str): The new password for the customer.

        Returns:
            bool: True if the password is changed successfully, False otherwise.
        """
        url = self._urls.customers.change_password
        params = {
            "customer-id": customer_id,
            "new-passwd": new_password,
        }
        return bool(self._post(url, params))
