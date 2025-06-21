import pytest

from .fixtures.db import reset_db
from .fixtures.users import (
    test_users,
    access_and_refresh_tokens_test_user,
    access_and_refresh_tokens_test_admin,
    user_id_for_update_or_delete,
)
from main import app


@pytest.mark.asyncio
async def test_get_users_list_with_admin(
    test_users, access_and_refresh_tokens_test_admin
):
    access_token, refresh_token = access_and_refresh_tokens_test_admin
    request, response = await app.asgi_client.get(
        "/v1/users", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status == 200


@pytest.mark.asyncio
async def test_get_users_list_with_user(access_and_refresh_tokens_test_user):
    access_token, refresh_token = access_and_refresh_tokens_test_user
    request, response = await app.asgi_client.get(
        "/v1/users", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status == 403


@pytest.mark.asyncio
async def test_get_users_list_with_anon_user():
    request, response = await app.asgi_client.get(
        "/v1/users",
    )

    assert response.status == 401


@pytest.mark.asyncio
async def test_get_me_list_with_admin(access_and_refresh_tokens_test_admin):
    access_token, refresh_token = access_and_refresh_tokens_test_admin
    request, response = await app.asgi_client.get(
        "/v1/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status == 200


@pytest.mark.asyncio
async def test_get_me_list_with_user(access_and_refresh_tokens_test_user):
    access_token, refresh_token = access_and_refresh_tokens_test_user
    request, response = await app.asgi_client.get(
        "/v1/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status == 200


@pytest.mark.asyncio
async def test_get_me_list_with_anon_user():
    request, response = await app.asgi_client.get(
        "/v1/users/me",
    )

    assert response.status == 401


@pytest.mark.asyncio
async def test_create_user_list_with_admin(
    access_and_refresh_tokens_test_admin,
):
    access_token, refresh_token = access_and_refresh_tokens_test_admin
    request, response = await app.asgi_client.post(
        "/v1/users",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "email": "test1@test.com",
            "password": "test1234",
            "first_name": "test1",
            "last_name": "test1",
        },
    )

    assert response.status == 200


@pytest.mark.asyncio
async def test_create_user_list_with_user(access_and_refresh_tokens_test_user):
    access_token, refresh_token = access_and_refresh_tokens_test_user
    request, response = await app.asgi_client.post(
        "/v1/users",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "email": "test2@test.com",
            "password": "test1234",
            "first_name": "test2",
            "last_name": "test2",
        },
    )

    assert response.status == 403


@pytest.mark.asyncio
async def test_create_user_list_with_anon_user():
    request, response = await app.asgi_client.post(
        "/v1/users",
        json={
            "email": "test3@test.com",
            "password": "test1234",
            "first_name": "test3",
            "last_name": "test3",
        },
    )

    assert response.status == 401


@pytest.mark.asyncio
async def test_update_user_list_with_user(
    access_and_refresh_tokens_test_user, user_id_for_update_or_delete
):
    access_token, refresh_token = access_and_refresh_tokens_test_user
    request, response = await app.asgi_client.patch(
        f"/v1/users/{user_id_for_update_or_delete}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "first_name": "test5",
        },
    )

    assert response.status == 403


@pytest.mark.asyncio
async def test_update_user_list_with_anon_user(user_id_for_update_or_delete):
    request, response = await app.asgi_client.patch(
        f"/v1/users/{user_id_for_update_or_delete}",
        json={
            "password": "test4321",
            "last_name": "test5",
        },
    )

    assert response.status == 401


@pytest.mark.asyncio
async def test_update_user_list_with_admin(
    access_and_refresh_tokens_test_admin, user_id_for_update_or_delete
):
    access_token, refresh_token = access_and_refresh_tokens_test_admin
    request, response = await app.asgi_client.patch(
        f"/v1/users/{user_id_for_update_or_delete}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "password": "test4321",
        },
    )

    assert response.status == 200
    assert "id" in response.json
    assert "email" in response.json
    assert "full_name" in response.json


@pytest.mark.asyncio
async def test_delete_user_list_with_user(
    access_and_refresh_tokens_test_user, user_id_for_update_or_delete
):
    access_token, refresh_token = access_and_refresh_tokens_test_user
    request, response = await app.asgi_client.delete(
        f"/v1/users/{user_id_for_update_or_delete}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status == 403


@pytest.mark.asyncio
async def test_delete_user_list_with_anon_user(user_id_for_update_or_delete):
    request, response = await app.asgi_client.delete(
        f"/v1/users/{user_id_for_update_or_delete}"
    )

    assert response.status == 401


@pytest.mark.asyncio
async def test_delete_user_list_with_admin(
    access_and_refresh_tokens_test_admin, user_id_for_update_or_delete
):
    access_token, refresh_token = access_and_refresh_tokens_test_admin
    request, response = await app.asgi_client.delete(
        f"/v1/users/{user_id_for_update_or_delete}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status == 204
