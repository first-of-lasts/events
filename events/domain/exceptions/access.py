from events.domain.exceptions.base import DomainError


class AuthenticationError(DomainError):
    ...


class ActionPermissionError(DomainError):
    ...
