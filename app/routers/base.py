from fastapi import APIRouter, HTTPException, status
from schemas.subscribes import Subscribe, SubscribeCreate

router = APIRouter(prefix="/subscribe", tags=["subscribe"])

fake_db = []

@router.get("/")
def get_sub():
    return fake_db

@router.post("/", response_model=Subscribe, status_code=201)
def add_subscribe(item: SubscribeCreate):
    new_id = max(x["id"] for x in fake_db) + 1 if fake_db else 1
    new_item = {"id": new_id, **item.model_dump()}
    fake_db.append(new_item)
    return new_item