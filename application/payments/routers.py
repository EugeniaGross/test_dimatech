from sanic.response import json
from sanic import Blueprint, Request, HTTPResponse
from sanic_ext import validate, openapi
from sqlalchemy.exc import IntegrityError
from sanic.log import logger

from payments.service import PaymentsService
from payments.schemes import PaymentCreateScheme, PaymentScheme
from users.models import Users
from utils.decorators import validate_signature, authorized

bp_payments = Blueprint(
    "Payments",
    "/payments",
)


@bp_payments.post("/")
@openapi.definition(
    body={
        "application/json": PaymentCreateScheme.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    }
)
@validate(json=PaymentCreateScheme)
@validate_signature()
async def create_payment(
    request: Request, body: PaymentCreateScheme
) -> HTTPResponse:
    payments_service: PaymentsService = request.app.ctx.payments_service
    try:
        await payments_service.create_payment(body)
    except IntegrityError as e:
        logger.error(e)
        return json(
            {"status": "Bad request", "message": "Incorrect data"}, status=400
        )
    return json({"status": "ok"})


@bp_payments.get("/")
@openapi.definition(
    response=[
        {
            "application/json": list[
                PaymentScheme(
                    id=1,
                    transaction_id="c303282d-f2e6-46ca-a04a-35d3d873712d",
                    amount=100,
                    created_at="2025-06-21T00:00:00.56789",
                ).model_dump()
            ]
        }
    ],
    secured="token",
)
@authorized()
async def get_user_payments(request: Request, user: Users) -> HTTPResponse:
    payments_service: PaymentsService = request.app.ctx.payments_service
    payments = await payments_service.get_all_by_user_id(user.id)
    return json(
        [
            PaymentScheme.model_validate(payment).model_dump()
            for payment in payments
        ]
    )
