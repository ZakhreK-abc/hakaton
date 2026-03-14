from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Subscribes(Base):                    # ← Singular форма обычно лучше
    __tablename__ = "subscribes"          # ← логичное имя таблицы

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    name: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True
    )
    description: Mapped[str | None] = mapped_column(
        String(500), nullable=True        # ← обычно дают побольше места
    )
    price: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    rating: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.0   # ← default очень помогает
    )
    category: Mapped[str] = mapped_column(   # ← category, а не kategory
        String(100), nullable=False, index=True
    )