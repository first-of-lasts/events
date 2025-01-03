from events.domain.exceptions.base import DomainError


class EventNotFoundError(DomainError):
    ...


class EventCategoryNotFoundError(DomainError):
    ...
