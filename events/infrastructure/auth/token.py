from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Literal
from jose import jwt, JWTError

from events.domain.exceptions.access import AuthenticationError


Algorithm = Literal[
    "HS256", "HS384", "HS512",
    "RS256", "RS384", "RS512",
]


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    PASSWORD_RESET = "password_reset"
    ACCOUNT_VERIFICATION = "account_verification"


class JwtTokenProcessor:
    def __init__(
            self,
            secret: str,
            access_token_expires: timedelta,
            refresh_token_expires: timedelta,
            algorithm: Algorithm,
    ):
        self.secret = secret
        self.access_token_expires = access_token_expires
        self.refresh_token_expires = refresh_token_expires
        self.algorithm = algorithm

    def create_access_token(self, user_id: int) -> str:
        issued_at = datetime.now(timezone.utc)
        expires = issued_at + self.access_token_expires
        to_encode = {
            "exp": expires,
            "iat": issued_at,
            "sub": str(user_id),
            "type": TokenType.ACCESS.value,
        }
        return jwt.encode(
            to_encode, self.secret, algorithm=self.algorithm,
        )

    def create_password_reset_token(self, user_id: int) -> str:
        issued_at = datetime.now(timezone.utc)
        expires = issued_at + self.access_token_expires
        to_encode = {
            "exp": expires,
            "iat": issued_at,
            "sub": str(user_id),
            "type": TokenType.PASSWORD_RESET.value,
        }
        return jwt.encode(
            to_encode, self.secret, algorithm=self.algorithm,
        )

    def create_refresh_token(self, user_id: int) -> str:
        issued_at = datetime.now(timezone.utc)
        expires = issued_at + self.refresh_token_expires
        to_encode = {
            "exp": expires,
            "iat": issued_at,
            "sub": str(user_id),
            "type": TokenType.REFRESH.value,
        }
        return jwt.encode(
            to_encode, self.secret, algorithm=self.algorithm,
        )

    def verify_token(self, token: str, token_type: TokenType) -> int:
        try:
            payload = jwt.decode(token, self.secret, self.algorithm)
            if payload.get("type") != token_type.value:
                raise AuthenticationError("Invalid token type")
            return int(payload["sub"])
        except JWTError:
            raise AuthenticationError("Invalid token")


class JwtTokenVerifier:
    def __init__(
            self,
            secret: str,
            algorithm: Algorithm,
    ):
        self.secret = secret
        self.algorithm = algorithm

    def verify_token(self, token: str, token_type: TokenType) -> int:
        try:
            payload = jwt.decode(token, self.secret, self.algorithm)
            if payload.get("type") != token_type.value:
                raise AuthenticationError("Invalid token type")
            return int(payload["sub"])
        except JWTError:
            raise AuthenticationError("Invalid token")
