from pydantic import BaseModel

class SubscribeBase(BaseModel):
    name: str
    prise: float
    kategory: str
    raeting: float
    description: str
    
class Subscribe(SubscribeBase):
    id: int

    class Config:
        from_attributes = True


class SubscribeCreate(SubscribeBase):
    pass