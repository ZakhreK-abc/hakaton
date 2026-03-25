from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.analytics import get_user_yearly_spending

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/yearly-spending")
async def user_yearly_spending(
    user_id: int = Query(..., description="ID пользователя"),
    year: int = Query(None, description="Год (если не указан — текущий)"),
    db: AsyncSession = Depends(get_db)
):
    data = await get_user_yearly_spending(db, user_id, year)
    return data