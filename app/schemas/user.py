from pydantic import BaseModel, Field, ConfigDict

class UserBase(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=20)
    mail: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=100)

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserLogin(BaseModel):
    mail: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=100)

class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)