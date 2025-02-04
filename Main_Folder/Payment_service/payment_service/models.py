from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from datetime import datetime

class Payment(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    order_id: int  # Corresponds to the order
    user_id: int  # Corresponds to the user making the payment
    total_amount: int  # Added to match .proto
    status: str  # E.g., "paid", "refunded", etc.
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()  # Ensure datetime is properly serialized
        }
class Refund(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    payment_id: int  # Corresponds to the payment
    refunded_amount: float
    refund_reason: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
class PaymentResponseModel(BaseModel):
    id: int
    order_id: int
    user_id: int
    total_amount: float
    status: str
    timestamp: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if isinstance(v, datetime) else v
        }