from pydantic import BaseModel

# Pydantic model for the incoming order data
class CreateOrder(BaseModel):
    user_id: int  # Assuming each order is associated with a user
    product_id: int
    quantity: int
    total_price: float  # Assuming total price is calculated and sent

# Model for updating order status
class UpdateOrder(BaseModel):
    status: str  # This is an example; adjust fields as per your requirements
