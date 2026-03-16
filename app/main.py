from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import base
from app.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # только для dev
    yield
    await engine.dispose()


app = FastAPI(
    title="API Сервер подписок",
    version="1.0",
    lifespan=lifespan,
)

app.include_router(base.router, prefix="/api")


@app.get("/")
def home():
    return {"message": "home"}   # исправил опечатку "messege"