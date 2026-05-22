from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TransactionBase(BaseModel):
    amount: float
    type: str
    description: Optional[str] = None
    recipient: Optional[str] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionOut(TransactionBase):
    id: int
    user_id: int
    currency: str
    status: str
    card_number: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True