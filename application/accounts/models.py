from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, NUMERIC, CheckConstraint

from database import Base

if TYPE_CHECKING:
    from users.models import Users


class Accounts(Base):
    __tablename__ = "accounts"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[float] = mapped_column(NUMERIC(15, 2))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    user: Mapped["Users"] = relationship(back_populates="accounts")

    __table_args__ = (
        CheckConstraint("balance > 0", name="check_balance_positive"),
    )
