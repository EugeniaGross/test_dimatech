from users.exceptions import UserNotFoundError, VerifyPasswordError
from users.repository import UsersAbstractRepository
from users.schemes import UserCreateScheme, UserLoginSchemes, UserUpdateScheme
from utils.hashes import HashService


class UserService:

    def __init__(
        self, repo: UsersAbstractRepository, hash_service: HashService
    ):
        self.repo: UsersAbstractRepository = repo
        self.hash_service: HashService = hash_service

    async def add_one(self, user: UserCreateScheme):
        user = user.model_dump()
        hash_password = self.hash_service.create_hash_password(
            user["password"]
        )
        user["hash_password"] = hash_password
        del user["password"]
        user = await self.repo.add_one(user)
        return user

    async def get_one(self, id: int):
        return await self.repo.get_one(id)

    async def get_all(self):
        return await self.repo.get_all()

    async def get_one_by_email(self, email: str):
        return await self.repo.get_one_by_email(email)

    async def authenticate_user(self, auth_user: UserLoginSchemes):
        user = await self.get_one_by_email(auth_user.email)
        if user is None:
            raise UserNotFoundError("Пользователь не найден")
        if not self.hash_service.verify_password(
            auth_user.password, user.hash_password
        ):
            raise VerifyPasswordError("Пароль введен не верно")
        return user

    async def delete_one(self, id: int):
        await self.repo.delete_one(id)

    async def update_one(self, id: int, data: UserUpdateScheme):
        data = data.model_dump(exclude_unset=True)
        if "password" in data:
            data["hash_password"] = self.hash_service.create_hash_password(
                data["password"]
            )
            del data["password"]
        user = await self.repo.update_one(id, data)
        return user
