from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
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
    
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", 
        back_populates="user", 
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.nickname}>"