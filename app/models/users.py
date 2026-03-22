from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    nickname: Mapped[str] = mapped_column(
        String(20), nullable=False, index=True
    )
    mail: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True
    )
    password: Mapped[str] = mapped_column(
        String(100000), nullable=False, index=True
    )
    