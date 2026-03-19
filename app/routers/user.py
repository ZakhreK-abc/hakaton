from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserUpdate, UserLogin, User
from app.models.users import Users
from app.database import get_db

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/login", response_model=dict)
async def login(
    creds: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    # Ищем пользователя по почте
    result = await db.execute(
        select(Users).where(Users.mail == creds.mail)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )

    # Здесь должна быть проверка пароля (bcrypt, argon2 и т.д.)
    # Сейчас просто заглушка — в реальности так НЕЛЬЗЯ!
    if user.password != creds.password:  # ← опасно! хранить пароли в plaintext нельзя
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )

    return {"verify": True, "user_id": user.id, "nickname": user.nickname}

# @router.get("/", response_model=User)
# async def get_user(user: Annotated[dict, Depends(get_user)], db: AsyncSession = Depends(get_db)):
#     mail = await db.execute(select(Users).where(Users.mail == user["mail"]))
#     password = await db.execute(select(Users).where(Users.password == user["password"]))
#     mail_item = mail.scalar_one_or_none()
#     password_item = password.scalar_one_or_none()

#     if mail_item is None or password_item is None:
#         raise HTTPException(status_code=404, detail="Неправельный пароль или почта")
    
#     elif mail == mail_item and password == password_item:
#         return {"verefy": True}

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(new_user: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. Проверка уникальности почты
    result = await db.execute(select(Users).where(Users.mail == new_user.mail))
    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Учётная запись с таким адресом почты уже существует"
        )

    # 2. Очень простая проверка формата почты (лучше использовать pydantic валидатор)
    if "@" not in new_user.mail or "." not in new_user.mail.split("@")[-1]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Некорректный адрес электронной почты"
        )

    # 3. Создание пользователя
    db_item = Users(**new_user.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)

    return db_item
    
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Users).where(Users.id == user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    await db.delete(user)
    await db.commit()
    return None