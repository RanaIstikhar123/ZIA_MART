from sqlmodel import SQLModel
from typing import Optional
class ProductCreate(SQLModel):
    name: str
    description: str
    price: float
    quantity: int

class ProductUpdate(SQLModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    quantity: Optional[int]
