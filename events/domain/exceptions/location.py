from events.domain.exceptions.base import DomainError


class CountryNotFoundError(DomainError):
    ...


class RegionNotFoundError(DomainError):
    ...


class InvalidRegionError(DomainError):
    ...
