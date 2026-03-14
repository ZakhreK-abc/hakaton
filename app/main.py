from fastapi import FastAPI
from app.routers import base
from app.database import engine, Base
import asyncio

app = FastAPI(
    title="Магазин API",
    version="1.0"
    )

app.include_router(base.router, prefix="/api")

@app.get("/")
def home():
    return {"messege": "home"}

# Создаём таблицы при старте (только для разработки!)
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)   # если нужно чистить
        await conn.run_sync(Base.metadata.create_all)