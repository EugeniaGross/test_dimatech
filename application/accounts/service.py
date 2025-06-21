from accounts.repository import AccountsAbstractRepository


class AccountsService:

    def __init__(
        self,
        repo: AccountsAbstractRepository,
    ):
        self.repo: AccountsAbstractRepository = repo

    async def get_all_by_user_id(self, user_id: int):
        accounts = await self.repo.get_all_by_user(user_id)
        return accounts
