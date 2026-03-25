from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import random
from fastapi import HTTPException

from app.models.subscribes import Subscribes
from app.models.transaction import Transaction


async def generate_fake_transaction(
    user_id: int,
    subscribe_id: int,           # переименовал для ясности
    db: AsyncSession             # db передаём извне, без Depends
):
    """
    Создаёт одну фейковую транзакцию на основе существующей подписки
    """
    # Получаем подписку по ID
    result = await db.execute(
        select(Subscribes).where(Subscribes.id == subscribe_id)
    )
    subscribe = result.scalar_one_or_none()

    if subscribe is None:
        raise HTTPException(404, f"Подписка с id={subscribe_id} не найдена")

    # Создаём новую транзакцию на основе подписки
    tx = Transaction(
        user_id=user_id,
        service_name=subscribe.name,
        amount=subscribe.price,
        currency="RUB",
        transaction_date=datetime.utcnow(),
        payment_method="ЮMoney",
        description=f"Оплата подписки {subscribe.name}",
        is_recurring=random.choice([True, False, False, False]),
        category=subscribe.category
    )

    db.add(tx)
    await db.commit()
    await db.refresh(tx)        # важно для получения id и свежих данных

    print(f"✅ Создана фейковая транзакция для пользователя {user_id} | "
          f"{subscribe.name} | {subscribe.price} ₽")

    return tx