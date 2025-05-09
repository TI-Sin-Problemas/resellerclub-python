"""Customer models"""

import typing as t
from dataclasses import dataclass
from datetime import datetime


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


@dataclass
class BaseCustomer:
    """
    Base class for Customer objects.

    Contains the common fields for customer objects.
    """

    username: str
    name: str
    company: str
    address: Address
    _id: t.Optional[str] = None

    @property
    def id(self):
        """Unique identifier of the customer."""
        return self._id


class CustomerPhones(t.NamedTuple):
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
        phones: CustomerPhones,
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
        super().__init__(username=username, name=name, company=company, address=address)
        self.password = password
        self.phones = phones
        self.language_code = language_code
        self.sms_consent = sms_consent
        self.vat_number = vat_number
        self.accept_policy = accept_policy
        self.marketing_consent = marketing_consent


class TwoFactorAuth(t.NamedTuple):
    """
    TwoFactorAuth constructor.

    Args:
        is_sms_enabled (bool): SMS 2FA enabled
        is_google_enabled (bool): Google Authenticator enabled
        is_2fa_enabled (bool): 2FA enabled
    """

    is_sms_enabled: bool
    is_google_enabled: bool
    is_2fa_enabled: bool


class Customer(BaseCustomer):
    """
    Represents a customer object.

    Args:
        _id (str): The unique identifier of the customer.
        username (str): Username for the Customer Account. Username should be an email address.
        reseller_id (str): Reseller Id of the Parent Reseller.
        name (str): Name of the Customer
        company (str): Name of the Customer's company.
        address (Address): Address of the Customer.
        total_receipts (float): The total amount of receipts for the customer.
        phone (str): The phone number of the customer.
        phone_country_code (str): The country code of the customer's phone number.
        status (str): The status of the customer (e.g. "Active", "Suspended", etc.).
        website_count (int): The number of websites associated with the customer.
        language_preference (str): The language preference of the customer.
        two_factor_auth (TwoFactorAuth): The two-factor authentication status of the customer.
        pin (str): The Personal Identification Number of the customer.
        is_password_expired (bool): Whether the customer's password has expired.
        user_email (str): The email address of the customer.
        creation_date (datetime): The creation date of the customer.
        sales_contact_id (str): The ID of the sales contact associated with the customer.

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
        address: Address,
        total_receipts: float,
        phones: CustomerPhones,
        status: str,
        website_count: int = None,
        language_preference: str = None,
        two_factor_auth: TwoFactorAuth = None,
        pin: str = None,
        is_password_expired: bool = None,
        user_email: str = None,
        creation_date: datetime = None,
        sales_contact_id: str = None,
    ):
        super().__init__(
            _id=_id, username=username, name=name, company=company, address=address
        )
        self.reseller_id = reseller_id
        self.status = status
        self.total_receipts = total_receipts
        self.phones = phones
        self.website_count = website_count
        self.language_preference = language_preference
        self.two_factor_auth = two_factor_auth
        self.pin = pin
        self.is_password_expired = is_password_expired
        self.user_email = user_email
        self.creation_date = creation_date
        self.sales_contact_id = sales_contact_id

    @classmethod
    def from_search(cls, data: dict):
        """
        Create a Customer object from a dictionary returned by the ResellerClub API search endpoint.

        Args:
            data: A dictionary as returned by the ResellerClub API.

        Returns:
            Customer: A Customer object.
        """
        customer_data = {k.split(".")[1]: v for k, v in data.items()}
        address = Address(
            line1=None,
            city=customer_data["city"],
            state=None,
            country=customer_data["country"],
            zip_code=None,
            other_state=None,
        )
        phones = CustomerPhones(
            phone_country_code=customer_data["telnocc"], phone=customer_data["telno"]
        )
        return cls(
            _id=customer_data["customerid"],
            username=customer_data["username"],
            reseller_id=customer_data["resellerid"],
            name=customer_data["name"],
            company=customer_data["company"],
            address=address,
            status=customer_data["customerstatus"],
            total_receipts=float(customer_data["totalreceipts"]),
            phones=phones,
            website_count=int(customer_data["websitecount"]),
        )

    @classmethod
    def from_details(cls, data: dict):
        """Create a Customer object from a dictionary returned by the ResellerClub API details
        endpoint.

        Args:
            data: A dictionary as returned by the ResellerClub API.

        Returns:
            Customer: A Customer object.
        """
        address = Address(
            line1=data["address1"],
            city=data["city"],
            state=data["state"],
            country=data["country"],
            zip_code=data["zip"],
            other_state=data["other_state"],
            line2=data.get("address2"),
            line3=data.get("address3"),
        )
        two_factor_auth = TwoFactorAuth(
            is_sms_enabled=bool(data["twofactorsmsauth_enabled"]),
            is_google_enabled=bool(data["twofactorgoogleauth_enabled"]),
            is_2fa_enabled=bool(data["twofactorauth_enabled"]),
        )
        phones = CustomerPhones(phone_country_code=data["telnocc"], phone=data["telno"])
        return cls(
            _id=data["customerid"],
            username=data["username"],
            reseller_id=data["resellerid"],
            name=data["name"],
            company=data["company"],
            address=address,
            total_receipts=float(data["totalreceipts"]),
            phones=phones,
            status=data["customerstatus"],
            language_preference=data["langpref"],
            two_factor_auth=two_factor_auth,
            pin=data["pin"],
            is_password_expired=bool(data["ispasswdexpired"]),
            user_email=data["useremail"],
            creation_date=datetime.fromtimestamp(int(data["creationdt"])),
            sales_contact_id=data["salescontactid"],
        )
