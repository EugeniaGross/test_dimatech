from datetime import datetime, timezone, timedelta

from jose import JWTError, jwt

from settings import settings


class JWTTokenService:

    @classmethod
    def create_access_and_refresh_tokens(cls, data: dict):
        access_token = cls._create_jwt_token(
            data,
            "access",
            settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        refresh_token = cls._create_jwt_token(
            data,
            "refresh",
            settings.REFRESH_TOKEN_EXPIRE_DAYS,
        )
        return access_token, refresh_token

    @staticmethod
    def _create_jwt_token(data: dict, type: str, token_expire: int):
        if type == "access":
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=token_expire
            )
        if type == "refresh":
            expire = datetime.now(timezone.utc) + timedelta(days=token_expire)
        data.update({"exp": expire, "type": type})
        token = jwt.encode(
            data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return token

    @staticmethod
    def decode_jwt_token(token: str):
        try:
            decode_token = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
        except (JWTError, AttributeError):
            return None
        if set(decode_token.keys()) != {"id", "exp", "type"}:
            return None
        return decode_token
