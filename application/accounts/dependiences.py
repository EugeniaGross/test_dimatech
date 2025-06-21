from accounts.repository import AccountsPostgreSQLRepository
from accounts.service import AccountsService


def accounts_service():
    return AccountsService(AccountsPostgreSQLRepository)
