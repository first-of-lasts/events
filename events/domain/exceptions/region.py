from events.domain.exceptions.base import DomainError


class RegionNotFoundError(DomainError):
    ...


class InvalidRegionError(DomainError):
    ...
