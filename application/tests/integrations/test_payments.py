import hashlib

import pytest

from .fixtures.db import reset_db
from .fixtures.users import (
    test_users,
    access_and_refresh_tokens_test_user,
    access_and_refresh_tokens_test_admin,
)
from accounts.models import Accounts
from database import async_session
from main import app
from settings import settings


@pytest.mark.asyncio
async def test_create_payment_with_invalid_signature(test_users):
    data = {
        "transaction_id": "5eae174f-7cd0-472c-bd36-35660f00132b",
        "user_id": 1,
        "account_id": 1,
        "amount": 100,
    }
    data["signature"] = hashlib.sha256(
        f"{data.get("account_id")}{data.get("amount")}{data.get("transaction_id")}{data.get("user_id")}dsfdsgdsgb4vd".encode()
    ).hexdigest()
    request, response = await app.asgi_client.post("/v1/payments", json=data)

    assert response.status == 400


@pytest.mark.asyncio
async def test_create_payment_with_valid_signature():
    data = {
        "transaction_id": "5eae174f-7cd0-472c-bd36-35660f00132b",
        "user_id": 1,
        "account_id": 1,
        "amount": 100,
    }
    data["signature"] = hashlib.sha256(
        f"{data.get("account_id")}{data.get("amount")}{data.get("transaction_id")}{data.get("user_id")}{settings.SIGNATURE_SECRET_KEY}".encode()
    ).hexdigest()
    request, response = await app.asgi_client.post("/v1/payments", json=data)
    async with async_session() as session:
        account = await session.get(Accounts, 1)

    assert response.status == 200
    assert account is not None


@pytest.mark.asyncio
async def test_create_payment_with_exsist_transaction():
    data = {
        "transaction_id": "5eae174f-7cd0-472c-bd36-35660f00132b",
        "user_id": 1,
        "account_id": 1,
        "amount": 100,
    }
    data["signature"] = hashlib.sha256(
        f"{data.get("account_id")}{data.get("amount")}{data.get("transaction_id")}{data.get("user_id")}{settings.SIGNATURE_SECRET_KEY}".encode()
    ).hexdigest()
    request, response = await app.asgi_client.post("/v1/payments", json=data)

    assert response.status == 400


@pytest.mark.asyncio
async def test_get_user_payments_with_admin(
    access_and_refresh_tokens_test_admin,
):
    access_token, refresh_token = access_and_refresh_tokens_test_admin
    request, response = await app.asgi_client.get(
        "/v1/payments", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status == 200


@pytest.mark.asyncio
async def test_get_user_payments_with_user(
    access_and_refresh_tokens_test_user,
):
    access_token, refresh_token = access_and_refresh_tokens_test_user
    request, response = await app.asgi_client.get(
        "/v1/payments", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status == 200


@pytest.mark.asyncio
async def test_get_user_payments_with_anon_user():
    request, response = await app.asgi_client.get(
        "/v1/payments",
    )

    assert response.status == 401
