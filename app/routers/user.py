from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserUpdate, UserLogin, UserOut
from app.models.users import Users
from app.database import get_db
from app.core.encryption import encryptor

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/login", response_model=dict)
async def login(
    creds: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    # 1. Ищем пользователя по почте
    result = await db.execute(
        select(Users).where(Users.mail == creds.mail)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )

    # 2. Расшифровываем пароль, которыALTER TABLE имя_таблицы DROP COLUMN имя_столбца;й лежит в базе
    try:
        decrypted_stored_password = encryptor.decrypt(user.password)
    except Exception as e:
        # Если расшифровка не удалась → скорее всего ключ неверный или данные повреждены
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка обработки учётных данных"
        )

    # 3. Сравниваем расшифрованный пароль из базы с тем, что прислал пользователь
    if decrypted_stored_password != creds.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )

    # 4. Успешный вход
    return {
        "verify": True,
        "user_id": user.id,
        "nickname": user.nickname
    }

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

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(new_user: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. Проверка уникальности почты
    result = await db.execute(select(Users).where(Users.mail == new_user.mail))
    if result.scalar_one_or_none() is not None:
        raise HTTPException(400, "Учётная запись с таким адресом почты уже существует")

    # 2. Шифруем пароль ПЕРЕД сохранением
    encrypted_password = encryptor.encrypt(new_user.password)

    # 3. Создаём объект с уже зашифрованным паролем
    db_item = Users(
        nickname=new_user.nickname,
        mail=new_user.mail,
        password=encrypted_password,          # ← здесь зашифрованный!
        # phone=new_user.phone,             # если тоже шифруешь — аналогично
        # другие поля...
    )

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