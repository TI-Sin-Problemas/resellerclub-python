"""Domain models for ResellerClub API"""

import typing as t


class Availability(t.NamedTuple):
    """Domain name availability for TLDs"""

    domain: str
    status: str
    classkey: str = None


class PremiumDomain(t.NamedTuple):
    """Premium Domain"""

    domain: str
    price: float


class Suggestion(t.NamedTuple):
    """Domain name suggestion"""

    domain: str
    status: str
    in_ga: bool
    score: float
    spin: str
