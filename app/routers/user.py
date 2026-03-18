from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserUpdate, User
from app.models.users import Users
from app.database import get_db

router = APIRouter(prefix="/user", tags=["user"])

router.get("/{nickname}", response_model=list[User])
async def get_user(nickname: str, db: AsyncSession = Depends(get_db),):
    result = await db.execute(select(Users).where(Users.nickname == nickname))
    db_item = result.scalar_one_or_none()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Пользователь не найдена")
    return db_item


