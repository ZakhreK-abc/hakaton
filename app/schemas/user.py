from pydantic import BaseModel, Field, ConfigDict, field_validator, field_serializer
from app.core.encryption import encryptor

class UserBase(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=20)
    mail: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=100)

class UserCreate(UserBase):
    @field_serializer("password", when_used="json")
    def encrypt_password(self, v: str | None) -> str | None:
        return encryptor.encrypt(v) if v else None

class UserUpdate(UserBase):
    pass

class UserLogin(BaseModel):
    mail: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=100)

class UserOut(UserBase):  # для ответа
    @field_validator("password", mode="after")
    @staticmethod
    def decrypt_password(cls, value: str | None) -> str | None:
        if value:
            try:
                return encryptor.decrypt(value)
            except Exception:
                return "[невозможно расшифровать]"
        return None

class User(UserBase):
    id: int