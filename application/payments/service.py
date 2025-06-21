from payments.repository import PaymentsAbstractRepository
from payments.schemes import PaymentCreateScheme
from settings import settings
from utils.hashes import HashService


class PaymentsService:

    def __init__(
        self, repo: PaymentsAbstractRepository, hash_service: HashService
    ):
        self.repo: PaymentsAbstractRepository = repo
        self.hash_service: HashService = hash_service

    async def get_all_by_user_id(self, user_id: int):
        payments = await self.repo.get_all_by_user(user_id)
        return payments

    async def create_payment(self, data: PaymentCreateScheme):
        await self.repo.add_one(data.model_dump())

    def is_valid_signature(self, data: PaymentCreateScheme):
        data = dict(sorted(data.model_dump().items()))
        signature = data.pop("signature")
        string = (
            "".join(map(str, data.values())) + settings.SIGNATURE_SECRET_KEY
        )
        return self.hash_service.is_valide_hash(string, signature)
