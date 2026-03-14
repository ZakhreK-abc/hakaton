from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.model import Subscribes
from app.database import get_db
from app.schemas.subscribes import SubscribeCreate, Subscribe

router = APIRouter(prefix="/subscribe", tags=["subscribe"])


@router.get("/", response_model=list[Subscribe])          # ← исправил
async def get_subscribes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Subscribes))
    return result.scalars().all()

@router.post("/", response_model=Subscribe, status_code=201)
async def create_subscribe(
    item: SubscribeCreate,
    db: AsyncSession = Depends(get_db)
):
    db_item = Subscribes(**item.model_dump())
    db.add(db_item)
    await db.commit()          # сначала сохраняем → появляется id
    await db.refresh(db_item)  # теперь можно безопасно обновить объект
    return db_item

# @router.post("/", response_model=Subscribe, status_code=201)
# async def create_subscribe(item: SubscribeCreate, db: AsyncSession = Depends(get_db)):
#     db_item = Subscribes(**item.model_dump())
#     db.add(db_item)
#     await db.refresh(db_item)
#     return db_item