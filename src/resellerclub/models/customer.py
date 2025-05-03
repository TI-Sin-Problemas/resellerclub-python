import typing as t
from dataclasses import dataclass


@dataclass
class BaseCustomer:
    """
    Base class for Customer objects.

    Contains the common fields for customer objects.
    """

    username: str
    name: str
    company: str
    _id: t.Optional[str] = None


class Address(t.NamedTuple):
    """
    Address constructor.

    Args:
        line1 (str): Address line 1 of the Customer's address
        city (str): City
        state (str): State. In case the State information is not available, you need to pass
            the value for this parameter as Not Applicable.
        country (str): Country Code as per ISO 3166-1 alpha-2
        zip_code (str): Zip code
        other_state (str, optional): This parameter needs to be included if the State
            information is not available. Defaults to None.
        line2 (str, optional): Address line 2 of the Customer's address. Defaults to None.
        line3 (str, optional): Address line 3 of the Customer's address. Defaults to None.
    """

    line1: str
    city: str
    state: str
    country: str
    zip_code: str
    other_state: str = None
    line2: str = None
    line3: str = None


class NewCustomerPhones(t.NamedTuple):
    """
    Phone constructor.

    Args:
        phone_country_code (str): Telephone number Country Code
        phone (str): Phone number
        alt_phone_country_code (str, optional): Alternate phone country code. Defaults to None.
        alt_phone (str, optional): Alternate phone number. Defaults to None.
        mobile_country_code (str, optional): Mobile country code. Defaults to None.
        mobile (str, optional): Mobile number. Defaults to None.
        fax_country_code (str, optional): Fax country code. Defaults to None.
        fax (str, optional): Fax number. Defaults to None.
    """

    phone_country_code: str
    phone: str
    alt_phone_country_code: str = None
    alt_phone: str = None
    mobile_country_code: str = None
    mobile: str = None
    fax_country_code: str = None
    fax: str = None


class NewCustomer(BaseCustomer):
    """NewCustomer class"""

    def __init__(
        self,
        username: str,
        password: str,
        name: str,
        company: str,
        address: Address,
        phones: NewCustomerPhones,
        language_code: str,
        sms_consent: bool = None,
        vat_number: str = None,
        accept_policy: bool = None,
        marketing_consent: bool = None,
    ):
        """
        NewCustomer constructor.

        Args:
            username (str): Username for the Customer Account. Username should be an email address.
            password (str): Password for the Customer Account.
            name (str): Name of the customer
            company (str): Name of the Customer's company
            address (NewCustomerAddress): Address of the customer
            phones (NewCustomerPhones): Phones of the customer
            language_code (str): Language Code as per ISO
            sms_consent (bool, optional): In case of a US based customer, consent is required to
                receive renewal reminder SMSes. Defaults to None.
            vat_number (str, optional): VAT ID for EU VAT. Defaults to None.
            accept_policy (bool, optional): Accept Terms and Conditions and Privacy Policy to
                create an account. Defaults to None.
            marketing_consent (bool, optional): In case of EEA (European Economic Area) countries
                capture consent to receive marketing emails
        """
        super().__init__(username=username, name=name, company=company)
        self.password = password
        self.address = address
        self.phones = phones
        self.language_code = language_code
        self.sms_consent = sms_consent
        self.vat_number = vat_number
        self.accept_policy = accept_policy
        self.marketing_consent = marketing_consent


class Customer(BaseCustomer):
    """
    Represents a customer object.

    Args:
        username (str): Username for the Customer Account. Username should be an email address.
        name (str): Name of the Customer
        company (str): Name of the Customer's company.
        city (str): City.
        state (str): State. In case the State information is not available, you need to pass the
            value for this parameter as Not Applicable.
        password (str): Password for the Customer Account.
        id (str): The unique identifier of the customer.
        reseller_id (str): Reseller Id of the Parent Reseller.
        state (str): The state of the customer.
        country (str): The country of the customer.
        status (str): The status of the customer (e.g. "Active", "Suspended", etc.).
        total_receipts (float): The total amount of receipts for the customer.
        phone (str): The phone number of the customer.
        phone_country_code (str): The country code of the customer's phone number.
        website_count (int): The number of websites associated with the customer.

    Returns:
        Customer: A Customer object.
    """

    def __init__(
        self,
        _id: str,
        username: str,
        reseller_id: str,
        name: str,
        company: str,
        city: str,
        state: str,
        country: str,
        total_receipts: float,
        phone: str,
        phone_country_code: str,
        status: str,
        website_count: int,
    ):
        super().__init__(_id=_id, username=username, name=name, company=company)
        self.reseller_id = reseller_id
        self.city = city
        self.state = state
        self.country = country
        self.status = status
        self.total_receipts = total_receipts
        self.phone = phone
        self.phone_country_code = phone_country_code
        self.website_count = website_count

    @classmethod
    def from_search(cls, data: dict):
        """
        Create a Customer object from a dictionary returned by the ResellerClub API.

        Args:
            data: A dictionary as returned by the ResellerClub API.

        Returns:
            Customer: A Customer object.
        """
        customer_data = {k.split(".")[1]: v for k, v in data.items()}
        return cls(
            _id=customer_data["customerid"],
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
