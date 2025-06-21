from abc import ABC, abstractmethod

from sqlalchemy import select

from database import async_session
from accounts.models import Accounts
from payments.models import Payments


class PaymentsAbstractRepository(ABC):

    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_user():
        raise NotImplementedError


class PaymentsPostgreSQLRepository(PaymentsAbstractRepository):

    @staticmethod
    async def add_one(data: dict):
        async with async_session() as session:
            query = select(Accounts).where(
                Accounts.user_id == data["user_id"],
                Accounts.id == data["account_id"],
            )
            result = await session.execute(query)
            account = result.scalar_one_or_none()
            if account is None:
                account = Accounts(
                    **{
                        "id": data["account_id"],
                        "user_id": data["user_id"],
                        "balance": data["amount"],
                    }
                )
                session.add(account)
            else:
                account.balance += data["amount"]
            payments = Payments(
                **{
                    "amount": data["amount"],
                    "user_id": data["user_id"],
                    "transaction_id": data["transaction_id"],
                }
            )
            session.add(payments)
            await session.commit()

    @staticmethod
    async def get_all_by_user(user_id: int):
        async with async_session() as session:
            query = select(Payments).where(Payments.user_id == user_id)
            result = await session.execute(query)
            return result.scalars().all()
