import pytest_asyncio
from sqlalchemy import select

from database import async_session
from users.models import Users
from users.utils import JWTTokenService


@pytest_asyncio.fixture()
async def test_users():
    async with async_session() as session:
        users = [
            Users(
                email="testuser@test.com",
                hash_password="$2b$12$jY7D8CoOfJSRrrLDx8kXbuyPXvP02g.7SlcNLsST13S238ji.a.gy",
                last_name="Popov",
                first_name="Max",
                middle_name="Petrovich",
            ),
            Users(
                email="testuser2@test.com",
                hash_password="$2b$12$jY7D8CoOfJSRrrLDx8kXbuyPXvP02g.7SlcNLsST13S238ji.a.gy",
                last_name="Ivanov",
                first_name="Maxim",
                middle_name="Ivanovich",
            ),
            Users(
                email="testadmin@test.com",
                hash_password="$2b$12$jY7D8CoOfJSRrrLDx8kXbuyPXvP02g.7SlcNLsST13S238ji.a.gy",
                last_name="Petrov",
                first_name="Alex",
                middle_name="Popovich",
                is_admin=True,
            ),
        ]
        session.add_all(users)
        await session.commit()


@pytest_asyncio.fixture()
async def access_and_refresh_tokens_test_admin():
    async with async_session() as session:
        query = select(Users).where(Users.email == "testadmin@test.com")
        result = await session.execute(query)
        user = result.scalars().one()
        return JWTTokenService.create_access_and_refresh_tokens(
            {"id": user.id}
        )


@pytest_asyncio.fixture()
async def access_and_refresh_tokens_test_user():
    async with async_session() as session:
        query = select(Users).where(Users.email == "testuser@test.com")
        result = await session.execute(query)
        user = result.scalars().one()
        return JWTTokenService.create_access_and_refresh_tokens(
            {"id": user.id}
        )


@pytest_asyncio.fixture()
async def user_id_for_update_or_delete():
    async with async_session() as session:
        query = select(Users).where(Users.email == "testuser2@test.com")
        result = await session.execute(query)
        user = result.scalars().one()
        return user.id
