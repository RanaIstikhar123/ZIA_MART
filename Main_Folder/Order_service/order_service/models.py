# models.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Order(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int  # Added to match .proto
    product_id: int
    quantity: int
    total_price: float  # Added to match .proto
    status: str  # E.g., "pending", "completed", matching .proto
    action: str  # E.g., "created", "updated", "deleted"
    # created_at: datetime = Field(default_factory=datetime.utcnow)
    # updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProductCache(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  
    description: str  
    price: int  
    quantity: int 
    