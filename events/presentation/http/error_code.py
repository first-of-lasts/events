from typing import Type

from events.domain.exceptions.access import AuthenticationError
from events.domain.exceptions.user import UserCannotBeCreatedError, UserNotFoundError
from events.domain.exceptions.location import CountryNotFoundError, RegionNotFoundError, InvalidRegionError


ERROR_CODE: dict[Type[Exception], int] = {
    AuthenticationError: 401,
    UserCannotBeCreatedError: 409,
    #
    UserNotFoundError: 404,
    CountryNotFoundError: 404,
    RegionNotFoundError: 404,
    InvalidRegionError: 400,
}
