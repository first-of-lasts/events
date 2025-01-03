from typing import Type

from events.domain.exceptions.access import AuthenticationError, ActionPermissionError
from events.domain.exceptions.user import UserCannotBeCreatedError, UserNotFoundError
from events.domain.exceptions.location import CountryNotFoundError, RegionNotFoundError, InvalidRegionError
from events.domain.exceptions.event import EventNotFoundError, EventCategoryNotFound


ERROR_CODE: dict[Type[Exception], int] = {
    AuthenticationError: 401,
    UserCannotBeCreatedError: 409,
    #
    ActionPermissionError: 403,
    UserNotFoundError: 404,
    CountryNotFoundError: 404,
    RegionNotFoundError: 404,
    InvalidRegionError: 400,
    EventNotFoundError: 404,
    EventCategoryNotFound: 404,
}
