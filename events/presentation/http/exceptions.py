from fastapi import Request
from fastapi.responses import JSONResponse

from events.domain.exceptions.base import DomainError
from events.presentation.http.error_code import ERROR_CODE


def get_http_error_response(
    err: DomainError,
    message: str,
) -> JSONResponse:
    return JSONResponse(
        status_code=ERROR_CODE.get(type(err), 500),
        content={"message": message}
    )


async def app_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, DomainError):
        return get_http_error_response(exc, exc.message)
    print(exc)
    return JSONResponse(status_code=500, content={})
