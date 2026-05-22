from sqlalchemy import String, Integer, Numeric, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Новые поля для банковской карты
    card_number: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)
    card_expiry: Mapped[str | None] = mapped_column(String(7), nullable=True)      # "12/28"
    card_holder: Mapped[str | None] = mapped_column(String(100), nullable=True)
    balance: Mapped[float] = mapped_column(Numeric(15, 2), default=50000.00)

    # Связи
    subscribes: Mapped[list["Subscribes"]] = relationship("Subscribes", back_populates="user", cascade="all, delete-orphan")
    transactions: Mapped[list["Transaction"]] = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"