from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.subscribe import SubscribeCreate, SubscribeUpdate, Subscribe
from app.models.subscribes import Subscribes
from app.database import get_db


router = APIRouter(prefix="/subscribe", tags=["subscribe"])


@router.get("/", response_model=list[Subscribe])          # ← исправил
async def get_all_subscribes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Subscribes))
    return result.scalars().all()

@router.get("/{Subscribe_id}", response_model=Subscribe)
async def get_subscribe(subscribe_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Subscribes).where(Subscribes.id == subscribe_id))
    db_item = result.scalar_one_or_none()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Подписка не найдена")
    return db_item

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


@router.put("/{subscribe_id}", response_model=Subscribe)
async def update_subscribe(
    subscribe_id: int,
    subscribe_update: SubscribeUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Subscribes).where(Subscribes.id == subscribe_id))
    db_item = result.scalar_one_or_none()

    if db_item is None:
        raise HTTPException(status_code=404, detail="Подписка не найдена")
    
    update_data = subscribe_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)

    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.delete("/{subscribe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subscribe(subscribe_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Subscribes).where(Subscribes.id == subscribe_id))
    db_item = result.scalar_one_or_none()

    if db_item is None:
        raise HTTPException(status_code=404, detail="Подписка не найдена")

    await db.delete(db_item)
    await db.commit()
    return None   # 204 No Content не возвращает тело