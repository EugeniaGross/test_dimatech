from datetime import datetime
from typing import Union

from pydantic import UUID4

from utils.base_schemes import BaseScheme


class PaymentScheme(BaseScheme):
    id: int
    transaction_id: UUID4
    amount: Union[int, float]
    created_at: datetime


class PaymentCreateScheme(BaseScheme):
    transaction_id: UUID4
    account_id: int
    user_id: int
    amount: Union[int, float]
    signature: str
