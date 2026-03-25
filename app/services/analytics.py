from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from datetime import datetime
from typing import Dict, List

from app.models.transaction import Transaction


async def get_user_yearly_spending(
    db: AsyncSession,
    user_id: int,
    year: int = None
) -> Dict:
    """
    Подсчёт трат пользователя за год с группировкой по месяцам
    """
    if year is None:
        year = datetime.utcnow().year

    # Основной запрос: сумма трат по месяцам
    stmt = (
        select(
            extract('month', Transaction.transaction_date).label('month'),
            func.sum(Transaction.amount).label('total')
        )
        .where(Transaction.user_id == user_id)
        .where(extract('year', Transaction.transaction_date) == year)
        .group_by(extract('month', Transaction.transaction_date))
        .order_by(extract('month', Transaction.transaction_date))
    )

    result = await db.execute(stmt)
    monthly_data = result.all()

    # Преобразуем в удобный формат
    months_spending = {int(row.month): float(row.total) for row in monthly_data}

    # Заполняем все 12 месяцев (даже если трат не было)
    full_year = []
    total_year = 0.0

    for month in range(1, 13):
        amount = months_spending.get(month, 0.0)
        total_year += amount
        full_year.append({
            "month": month,
            "month_name": datetime(2025, month, 1).strftime("%B"),  # Январь, Февраль...
            "amount": round(amount, 2)
        })

    return {
        "year": year,
        "total_spent": round(total_year, 2),
        "monthly_spending": full_year,
        "transaction_count": len(monthly_data)  # сколько месяцев было трат
    }