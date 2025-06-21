from users.repository import UsersPostgreSQLRepository
from users.service import UserService
from utils.hashes import HashService


def users_service():
    return UserService(UsersPostgreSQLRepository, HashService())
