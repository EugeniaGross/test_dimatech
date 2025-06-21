from abc import ABC, abstractmethod

from sqlalchemy import select

from users.models import Users
from database import async_session


class UsersAbstractRepository(ABC):

    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def get_one():
        raise NotImplementedError

    @abstractmethod
    async def get_all():
        raise NotImplementedError

    @abstractmethod
    async def delete_one():
        raise NotImplementedError

    @abstractmethod
    async def update_one():
        raise NotImplementedError

    @abstractmethod
    async def get_one_by_email():
        raise NotImplementedError


class UsersPostgreSQLRepository(UsersAbstractRepository):

    @staticmethod
    async def add_one(data: dict):
        async with async_session() as session:
            user = Users(**data)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    @staticmethod
    async def get_one(id: int):
        async with async_session() as session:
            result = await session.get(Users, id)
            return result

    @staticmethod
    async def get_all():
        async with async_session() as session:
            query = select(Users)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_one_by_email(email: str):
        async with async_session() as session:
            query = select(Users).where(Users.email == email)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @staticmethod
    async def delete_one(id: int):
        async with async_session() as session:
            user = await session.get(Users, id)
            await session.delete(user)

    @staticmethod
    async def update_one(id: int, data: dict):
        async with async_session() as session:
            user = await session.get(Users, id)
            for key, value in data.items():
                setattr(user, key, value)
            await session.commit()
            await session.refresh(user)
            return user
