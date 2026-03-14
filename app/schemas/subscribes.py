from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class SubscribeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    rating: float = Field(default=0.0, ge=0, le=5)
    category: str = Field(..., min_length=1)


class SubscribeCreate(SubscribeBase):
    pass


class Subscribe(SubscribeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)