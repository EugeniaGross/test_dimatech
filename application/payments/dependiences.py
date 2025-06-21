from payments.repository import PaymentsPostgreSQLRepository
from payments.service import PaymentsService
from utils.hashes import HashService


def payments_service():
    return PaymentsService(PaymentsPostgreSQLRepository, HashService())
