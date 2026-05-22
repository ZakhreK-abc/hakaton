# Создай файл recreate.py и запусти
import asyncio
from app.database import engine, Base

async def recreate():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы пересозданы!")

asyncio.run(recreate())