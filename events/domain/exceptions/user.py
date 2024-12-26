from events.domain.exceptions.base import DomainError


class UserCannotBeCreatedError(DomainError):
    ...


class UserNotFoundError(DomainError):
    ...
