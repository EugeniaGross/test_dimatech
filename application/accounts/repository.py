from abc import ABC, abstractmethod

from sqlalchemy import select

from accounts.models import Accounts
from database import async_session


class AccountsAbstractRepository(ABC):

    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_user():
        raise NotImplementedError


class AccountsPostgreSQLRepository(AccountsAbstractRepository):

    @staticmethod
    async def add_one(data: dict):
        async with async_session() as session:
            account = Accounts(**data)
            session.add(account)
            await session.commit()
            await session.refresh(account)
            return account

    @staticmethod
    async def get_all_by_user(user_id: int):
        async with async_session() as session:
            query = select(Accounts).where(Accounts.user_id == user_id)
            result = await session.execute(query)
            return result.scalars().all()
