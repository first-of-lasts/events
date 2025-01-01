from fastapi import Request, HTTPException, Depends

from events.domain.exceptions.access import AuthenticationError
from events.infrastructure.auth.token import JwtTokenVerifier, TokenType
from events.main.config import Config


class JwtTokenAuthentication:
    def __init__(self, config: Config):
        self.jwt_token_verifier = JwtTokenVerifier(
            secret=config.app.jwt_secret,
            algorithm=config.app.jwt_secret_algorithm,
        )

    async def __call__(self, request: Request) -> int:
        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Unauthorized")
        try:
            user_id = self.jwt_token_verifier.verify_token(
                token=authorization.split("Bearer ")[1],
                token_type=TokenType.ACCESS,
            )
            return user_id
        except AuthenticationError:
            raise HTTPException(status_code=401, detail="Unauthorized")


def get_user_id(
        auth: JwtTokenAuthentication = Depends(JwtTokenAuthentication(Config()))
) -> JwtTokenAuthentication:
    return auth
