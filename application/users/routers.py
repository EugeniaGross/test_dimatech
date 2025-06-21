from sanic.response import json
from sanic import Blueprint, Request, HTTPResponse
from sanic_ext import validate
from sanic_ext import openapi
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from sanic.log import logger

from utils.decorators import authorized, is_admin
from users.exceptions import UserNotFoundError, VerifyPasswordError
from users.models import Users
from users.schemes import (
    UserCreateScheme,
    UserScheme,
    UserLoginSchemes,
    JWTTokenSchemes,
    UserUpdateScheme,
    JWTRefreshTokenSchemes,
)
from users.service import UserService
from users.utils import JWTTokenService

bp_users = Blueprint(
    "Users",
    "/users",
)

bp_auth = Blueprint(
    "Auth",
    "/",
)


@bp_auth.post("/login")
@openapi.definition(
    body={
        "application/json": UserLoginSchemes.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
    response=[
        {
            "application/json": JWTTokenSchemes.model_json_schema(
                ref_template="#/components/schemas/{model}"
            )
        }
    ],
)
@validate(json=UserLoginSchemes)
async def login(request: Request, body: UserLoginSchemes) -> HTTPResponse:
    users_service: UserService = request.app.ctx.users_service
    token_service: JWTTokenService = request.app.ctx.token_service
    try:
        user = await users_service.authenticate_user(body)
    except (UserNotFoundError, VerifyPasswordError) as e:
        logger.error(e)
        return json(
            {
                "description": "Bad request",
                "message": "Incorrect email or password",
            },
            status=400,
        )
    access_token, refresh_token = (
        token_service.create_access_and_refresh_tokens({"id": user.id})
    )
    tokens = JWTTokenSchemes(
        access_token=access_token, refresh_token=refresh_token
    )
    return json(tokens.model_dump())


@bp_auth.post("/refresh_token")
@openapi.definition(
    body={
        "application/json": JWTRefreshTokenSchemes.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
    response=[
        {
            "application/json": JWTTokenSchemes.model_json_schema(
                ref_template="#/components/schemas/{model}"
            )
        }
    ],
)
@validate(json=JWTRefreshTokenSchemes)
async def refresh_token(
    request: Request, body: JWTRefreshTokenSchemes
) -> HTTPResponse:
    users_service: UserService = request.app.ctx.users_service
    token_service: JWTTokenService = request.app.ctx.token_service
    decode_token = token_service.decode_jwt_token(body.refresh_token)
    if decode_token is None:
        return json(
            {"description": "Bad request", "message": "Invalid_token"},
            status=400,
        )
    user = await users_service.get_one(decode_token.get("id"))
    if user is None:
        return json(
            {"description": "Bad request", "message": "Invalid_token"},
            status=400,
        )
    access_token, refresh_token = (
        token_service.create_access_and_refresh_tokens({"id": user.id})
    )
    tokens = JWTTokenSchemes(
        access_token=access_token, refresh_token=refresh_token
    )
    return json(tokens.model_dump())


@bp_users.get("/")
@openapi.definition(
    response={
        "application/json": list[
            UserScheme(
                email="test@test.com", id=1, full_name="Smith Sam"
            ).model_dump()
        ]
    },
    secured="token",
)
@authorized()
@is_admin()
async def get_users(request: Request) -> HTTPResponse:
    users_service: UserService = request.app.ctx.users_service
    users = await users_service.get_all()
    return json(
        [UserScheme.model_validate(user).model_dump() for user in users]
    )


@bp_users.post("/")
@openapi.definition(
    body={
        "application/json": UserCreateScheme.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
    response=[
        {
            "application/json": UserScheme.model_json_schema(
                ref_template="#/components/schemas/{model}"
            )
        }
    ],
    secured="token",
)
@authorized()
@is_admin()
@validate(json=UserCreateScheme)
async def create_user(
    request: Request, body: UserCreateScheme
) -> HTTPResponse:
    users_service: UserService = request.app.ctx.users_service
    try:
        user = await users_service.add_one(body)
    except IntegrityError as e:
        logger.error(e)
        return json(
            {
                "description": "Bad request",
                "message": "The user with this email already exists",
            },
            status=400,
        )
    return json(UserScheme.model_validate(user).model_dump())


@bp_users.delete("/<user_id:int>")
@openapi.secured("token")
@authorized()
@is_admin()
async def delete_user(request: Request, user_id: int) -> HTTPResponse:
    users_service: UserService = request.app.ctx.users_service
    try:
        await users_service.delete_one(user_id)
    except UnmappedInstanceError as e:
        logger.error(e)
        return json(
            {"description": "Not Found", "message": "User no found"},
            status=404,
        )
    return json({"status": "ok"}, status=204)


@bp_users.patch("/<user_id:int>")
@openapi.definition(
    body={
        "application/json": UserUpdateScheme.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
    response=[
        {
            "application/json": UserScheme.model_json_schema(
                ref_template="#/components/schemas/{model}"
            )
        }
    ],
    secured="token",
)
@authorized()
@is_admin()
@validate(json=UserUpdateScheme)
async def update_user(
    request: Request, user_id: int, body: UserUpdateScheme
) -> HTTPResponse:
    users_service: UserService = request.app.ctx.users_service
    try:
        user = await users_service.update_one(user_id, body)
    except AttributeError as e:
        logger.error(e)
        return json(
            {"description": "Not Found", "message": "User no found"},
            status=404,
        )
    return json(UserScheme.model_validate(user).model_dump())


@bp_users.get("/me")
@openapi.definition(
    response=[
        {
            "application/json": UserScheme.model_json_schema(
                ref_template="#/components/schemas/{model}"
            )
        }
    ],
    secured="token",
)
@authorized()
async def get_current_user(request: Request, user: Users) -> HTTPResponse:
    return json(UserScheme.model_validate(user).model_dump())
