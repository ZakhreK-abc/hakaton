# app/routers/dev.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.transaction import Transaction
from app.services.fake_data import generate_fake_transaction
from sqlalchemy import select

router = APIRouter(prefix="/dev", tags=["development"])


@router.post("/generate-fake-transaction")
async def create_fake_transaction(
    user_id: int = Query(..., description="ID пользователя"),
    subscribe_id: int = Query(..., description="ID подписки, из которой брать данные"),
    db: AsyncSession = Depends(get_db)
):
    """
    Создаёт одну фейковую транзакцию на основе существующей подписки
    """
    transaction = await generate_fake_transaction(
        user_id=user_id,
        subscribe_id=subscribe_id,
        db=db
    )

    return {
        "status": "success",
        "message": f"Фейковая транзакция успешно создана для пользователя {user_id}",
        "transaction_id": transaction.id,
        "service_name": transaction.service_name,
        "amount": transaction.amount
    }

@router.get("/ear_spends/{user_id}")
async def get_ear_spends(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Transaction).where(Transaction.user_id == user_id)
    )
    