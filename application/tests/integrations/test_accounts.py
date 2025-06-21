import pytest

from .fixtures.db import reset_db
from .fixtures.users import (
    test_users,
    access_and_refresh_tokens_test_user,
    access_and_refresh_tokens_test_admin,
)
from main import app


@pytest.mark.asyncio
async def test_get_user_accounts_with_admin(
    test_users, access_and_refresh_tokens_test_admin
):
    access_token, refresh_token = access_and_refresh_tokens_test_admin
    request, response = await app.asgi_client.get(
        "/v1/accounts", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status == 200


@pytest.mark.asyncio
async def test_get_user_accounts_with_user(
    access_and_refresh_tokens_test_user,
):
    access_token, refresh_token = access_and_refresh_tokens_test_user
    request, response = await app.asgi_client.get(
        "/v1/accounts", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status == 200


@pytest.mark.asyncio
async def test_get_user_accounts_with_anon_user():
    request, response = await app.asgi_client.get(
        "/v1/accounts",
    )

    assert response.status == 401
