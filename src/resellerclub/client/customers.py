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

        url = self._urls.customers.get_search_url()
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
        data = self._get_data(url, params)

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
