from typing import Type

from events.domain.exceptions.access import AuthenticationError, ActionPermissionError
from events.domain.exceptions.user import UserCannotBeCreatedError, UserNotFoundError
from events.domain.exceptions.location import CountryNotFoundError, RegionNotFoundError, InvalidRegionError
from events.domain.exceptions.event import EventNotFoundError, EventCategoryNotFoundError
from events.domain.exceptions.attendee import AttendeeAlreadyExistsError


ERROR_CODE: dict[Type[Exception], int] = {
    AuthenticationError: 401,
    UserCannotBeCreatedError: 400,
    #
    ActionPermissionError: 403,
    UserNotFoundError: 404,
    CountryNotFoundError: 404,
    RegionNotFoundError: 404,
    InvalidRegionError: 400,
    EventNotFoundError: 404,
    EventCategoryNotFoundError: 404,
    AttendeeAlreadyExistsError: 400,
}
