from pydantic import BaseModel

class Subscribe(BaseModel):
    name: str
    prise: float
    kategory: str
    raeting: float
    description: str
    