from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from database import Base

from accounts.models import Accounts
from payments.models import Payments


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    middle_name: Mapped[Optional[str]] = mapped_column(String(255))
    hash_password: Mapped[str] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(default=False)

    accounts: Mapped[list[Accounts]] = relationship(back_populates="user")
    payments: Mapped[list[Payments]] = relationship(back_populates="user")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name} {self.middle_name if self.middle_name else ""}".strip()
