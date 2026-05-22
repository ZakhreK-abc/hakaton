from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.transactions import Transaction
from app.schemas.transaction import TransactionCreate, TransactionOut
import random
from datetime import datetime

router = APIRouter(prefix="/bank", tags=["bank"])

@router.get("/transactions/{user_id}", response_model=list[TransactionOut])
async def get_transactions(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Transaction).where(Transaction.user_id == user_id).order_by(Transaction.created_at.desc())
    )
    return result.scalars().all()


@router.post("/transfer", response_model=TransactionOut)
async def create_transfer(data: TransactionCreate, user_id: int, db: AsyncSession = Depends(get_db)):
    transaction = Transaction(
        user_id=user_id,
        amount=-abs(data.amount),
        type=data.type or "transfer",
        description=data.description,
        recipient=data.recipient,
    )
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction


# Фейковый генератор операций
@router.post("/generate-fake")
async def generate_fake_transactions(user_id: int, count: int = 10, db: AsyncSession = Depends(get_db)):
    types = ["payment", "transfer", "deposit", "subscription"]
    descriptions = ["Оплата Wildberries", "Перевод другу", "Зарплата", "Netflix", "Яндекс Плюс", "Пополнение карты"]

    for _ in range(count):
        tx = Transaction(
            user_id=user_id,
            amount=round(random.uniform(-5000, 80000), 2),
            type=random.choice(types),
            description=random.choice(descriptions),
            status="completed",
            created_at=datetime.utcnow()
        )
        db.add(tx)
    await db.commit()
    return {"message": f"Создано {count} фейковых операций"}