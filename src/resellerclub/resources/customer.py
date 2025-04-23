from typing import NamedTuple


class Customer(NamedTuple):
    """Customer object"""

    id: str = None
    username: str = None
    reseller_id: str = None
    name: str = None
    company: str = None
    city: str = None
    state: str = None
    country: str = None
    status: str = None
    total_receipts: float = None
    phone: str = None
    phone_country_code: str = None
    website_count: int = None

    @classmethod
    def from_api(cls, data: dict):
        """
        Create a Customer object from a dictionary returned by the ResellerClub API.

        Args:
            data: A dictionary as returned by the ResellerClub API.

        Returns:
            Customer: A Customer object.
        """
        customer_data = {k.split(".")[1]: v for k, v in data.items()}
        return cls(
            id=customer_data["customerid"],
            username=customer_data["username"],
            reseller_id=customer_data["resellerid"],
            name=customer_data["name"],
            company=customer_data["company"],
            city=customer_data["city"],
            state=customer_data.get("state"),
            country=customer_data["country"],
            status=customer_data["customerstatus"],
            total_receipts=float(customer_data["totalreceipts"]),
            phone=customer_data["telno"],
            phone_country_code=customer_data["telnocc"],
            website_count=int(customer_data["websitecount"]),
        )
