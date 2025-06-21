from typing import List
from sanic.response import json
from sanic import Blueprint, Request, HTTPResponse
from sanic_ext import openapi

from utils.decorators import authorized
from accounts.service import AccountsService
from accounts.schemes import AccountScheme
from users.models import Users

bp_accounts = Blueprint(
    "Accounts",
    "/accounts",
)


@bp_accounts.get("/")
@openapi.definition(
    response=[
        {
            "application/json": List[
                AccountScheme(id=1, balance=1000).model_dump()
            ]
        }
    ],
    secured="token",
)
@authorized()
async def get_user_accounts(request: Request, user: Users) -> HTTPResponse:
    accounts_service: AccountsService = request.app.ctx.accounts_service
    accounts = await accounts_service.get_all_by_user_id(user.id)
    return json(
        [
            AccountScheme.model_validate(account).model_dump()
            for account in accounts
        ]
    )
