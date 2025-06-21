import pytest

from .fixtures.db import reset_db
from .fixtures.users import (
    test_users,
    access_and_refresh_tokens_test_user,
    access_and_refresh_tokens_test_admin,
)
from main import app


@pytest.mark.asyncio
async def test_login_with_valid_data(test_users):
    request, response = await app.asgi_client.post(
        "/v1/login",
        json={"email": "testuser@test.com", "password": "12345678"},
    )

    assert response.status == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json


@pytest.mark.asyncio
async def test_refresh_token_with_valid_data_admin(
    access_and_refresh_tokens_test_admin,
):
    access_token, refresh_token = access_and_refresh_tokens_test_admin
    request, response = await app.asgi_client.post(
        "/v1/refresh_token", json={"refresh_token": refresh_token}
    )

    assert response.status == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json


@pytest.mark.asyncio
async def test_refresh_token_with_valid_data_user(
    access_and_refresh_tokens_test_user,
):
    access_token, refresh_token = access_and_refresh_tokens_test_user
    request, response = await app.asgi_client.post(
        "/v1/refresh_token", json={"refresh_token": refresh_token}
    )

    assert response.status == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json


@pytest.mark.asyncio
async def test_refresh_token_with_invalid():
    request, response = await app.asgi_client.post(
        "/v1/refresh_token", json={"refresh_token": "1234567890"}
    )

    assert response.status == 400


@pytest.mark.asyncio
async def test_login_with_invalid_data():
    request, response = await app.asgi_client.post(
        "/v1/login",
        json={"email": "test_user@test.com", "password": "87654321"},
    )

    assert response.status == 400
