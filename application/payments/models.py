from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UUID, CheckConstraint, NUMERIC, text

from database import Base

if TYPE_CHECKING:
    from users.models import Users


class Payments(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_id: Mapped[str] = mapped_column(UUID(), unique=True)
    amount: Mapped[float] = mapped_column(NUMERIC(15, 2))
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    user: Mapped["Users"] = relationship(back_populates="payments")

    __table_args__ = (
        CheckConstraint("amount > 0", name="check_amount_positive"),
    )
