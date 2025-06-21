from functools import wraps

from sanic.response import json

from payments.service import PaymentsService
from users.service import UserService
from users.utils import JWTTokenService


def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            users_service: UserService = request.app.ctx.users_service
            token_service: JWTTokenService = request.app.ctx.token_service
            access_token = request.token
            if access_token is None:
                return json({"description": "Unauthorized"}, 401)
            decode_token = token_service.decode_jwt_token(access_token)
            if decode_token is None or decode_token.get("type") != "access":
                return json({"description": "Unauthorized"}, 401)
            user = await users_service.get_one(decode_token.get("id"))
            if user is None:
                return json({"description": "Unauthorized"}, 401)
            response = await f(request, user=user, *args, **kwargs)
            return response

        return decorated_function

    return decorator


def is_admin():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            if not kwargs["user"].is_admin:
                return json({"description": "Forbidden"}, 403)
            del kwargs["user"]
            response = await f(request, *args, **kwargs)
            return response

        return decorated_function

    return decorator


def validate_signature():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            payments_service: PaymentsService = (
                request.app.ctx.payments_service
            )
            if not payments_service.is_valid_signature(kwargs["body"]):
                return json(
                    {
                        "description": "Bad request",
                        "message": "Invaid signature",
                    },
                    400,
                )
            response = await f(request, *args, **kwargs)
            return response

        return decorated_function

    return decorator
