from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from datetime import datetime
from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    service_name = Column(String(100), nullable=False)      # "Яндекс Плюс", "Netflix" и т.д.
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="RUB")
    transaction_date = Column(DateTime, default=datetime.utcnow)
    payment_method = Column(String(50), default="ЮMoney")   # ЮMoney, Сбер, Тинькофф и т.д.
    description = Column(String(255))
    is_recurring = Column(Boolean, default=False)           # регулярный платёж?
    category = Column(String(50), default="Подписка")       # Стриминг, Софт, Доставка и т.д.

    user = relationship("Users", back_populates="transactions")