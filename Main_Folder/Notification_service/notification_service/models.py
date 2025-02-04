from sqlmodel import SQLModel, Field
from datetime import datetime

class Notification(SQLModel, table=True):
    id: int = Field(default = None, primary_key=True)
    user_id: int  # Corresponds to the user receiving the notification
    message: str
    event_type: str  # E.g., "order_created", "payment_processed"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: str
