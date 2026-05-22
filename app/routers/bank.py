from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.transactions import Transaction
from app.models.users import Users
from app.schemas.transaction import TransactionOut
import random
from datetime import datetime

router = APIRouter(prefix="/bank", tags=["bank"])


@router.get("/transactions/{user_id}", response_model=list[TransactionOut])
async def get_transactions(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Transaction)
        .where(Transaction.user_id == user_id)
        .order_by(Transaction.created_at.desc())
    )
    return result.scalars().all()


@router.post("/generate-fake/{user_id}")
async def generate_fake_transactions(
    user_id: int, 
    count: int = 15, 
    db: AsyncSession = Depends(get_db)
):
    # Получаем пользователя
    user_result = await db.execute(select(Users).where(Users.id == user_id))
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Если у пользователя нет карты — генерируем
    if not user.card_number:
        user.card_number = f"4276 {random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}"
        user.card_expiry = f"{random.randint(1,12):02d}/{random.randint(27,30)}"
        user.card_holder = user.full_name.upper() if user.full_name else "IVAN IVANOV"
        await db.commit()

    transaction_types = ["payment", "transfer", "deposit", "withdrawal", "subscription"]
    descriptions = [
        "Оплата в Wildberries", "Перевод другу", "Зарплата", "Оплата Netflix",
        "Покупка в Steam", "Оплата ЖКХ", "Пополнение МТС", "Подписка Яндекс Плюс",
        "Перевод на карту", "Оплата в Ozon"
    ]

    for _ in range(count):
        amount = round(random.uniform(-25000, 80000), 2)
        tx_type = random.choice(transaction_types)

        transaction = Transaction(
            user_id=user_id,
            amount=amount,
            type=tx_type,
            description=random.choice(descriptions),
            recipient="Сбербанк" if tx_type == "transfer" else None,
            card_number=user.card_number,          # ← Берём карту пользователя
            status="completed",
            created_at=datetime.utcnow()
        )
        db.add(transaction)

    await db.commit()

    return {
        "status": "success",
        "message": f"Сгенерировано {count} фейковых транзакций",
        "user_card": user.card_number,
        "user_balance": float(user.balance)
    }