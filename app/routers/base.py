from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.model import Subscribes
from app.database import get_db
from app.schemas.subscribes import SubscribeCreate, Subscribe

router = APIRouter(prefix="/subscribe", tags=["subscribe"])

fake_db = []

@router.get("/", response_model=list[SubscribeCreate])
async def get_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Subscribes))
    return result.scalars().all()

@router.post("/", response_model=Subscribe, status_code=201)
async def create_subscribe(item: SubscribeCreate, db: AsyncSession = Depends(get_db)):
    db_item = Subscribes(**item.model_dump())
    db.add(db_item)
    # commit происходит автоматически в get_db после yield, если нет исключений
    await db.refresh(db_item)
    return db_item

# @router.get("/")
# def get_sub():
#     return fake_db

# @router.post("/", response_model=Subscribe, status_code=201)
# def add_subscribe(item: SubscribeCreate):
#     new_id = max(x["id"] for x in fake_db) + 1 if fake_db else 1
#     new_item = {"id": new_id, **item.model_dump()}
#     fake_db.append(new_item)
#     return new_item