from typing import Annotated, Optional

from pydantic import EmailStr, Field

from utils.base_schemes import BaseScheme


class EmailScheme(BaseScheme):
    email: EmailStr


class PasswordScheme(BaseScheme):
    password: Annotated[str, Field(min_length=8)]


class UserCreateScheme(EmailScheme, PasswordScheme):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None


class UserUpdateScheme(BaseScheme):
    email: Optional[EmailStr] = None
    password: Optional[Annotated[str, Field(min_length=8)]] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None


class UserLoginSchemes(EmailScheme, PasswordScheme):
    pass


class UserScheme(EmailScheme):
    id: int
    full_name: str


class JWTRefreshTokenSchemes(BaseScheme):
    refresh_token: str


class JWTTokenSchemes(JWTRefreshTokenSchemes):
    access_token: str
