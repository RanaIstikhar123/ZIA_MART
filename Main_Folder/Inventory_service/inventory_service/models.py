# models.py
from sqlmodel import SQLModel, Field
from typing import Optional

class Inventory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int
    stock: int = 100 # Represents the current stock level for the product


 # Initial stock of 100 units for every new product



