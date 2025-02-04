import logging
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from payment_service.kafka_utils import consume_order_messages
from payment_service.db import get_session, create_db_and_tables
from payment_service.crud import create_payment, create_refund, get_payment_by_id, get_payments_by_user, update_payment_status, delete_payment
import asyncio
from payment_service.models import PaymentResponseModel

logging.basicConfig(level=logging.INFO)

# Async lifespan for handling startup and shutdown processes
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating Database Tables")
    await create_db_and_tables()

    # Start Kafka consumer as a background task
    logging.info("Starting Kafka consumer task for order messages...")
    consume_task = asyncio.create_task(consume_order_messages())

    # Yield for FastAPI lifespan
    yield

    # Ensure task completes before shutdown
    await consume_task

# Initialize FastAPI app with lifespan management
app = FastAPI(
    lifespan=lifespan,
    title="Payment Service",
    version="0.0.1"
)

# Route to get all payments by a specific user
# Route to create a payment

@app.get("/")
def read_root():
    return {"Hello": "Payment Service"}
@app.post("/payments/")
async def create_payment_route(order_id: int, user_id: int, total_amount: float):
    async with get_session() as session:  # Explicitly creating session here
        payment = await create_payment(session, order_id, user_id, total_amount, status="paid")
        return payment

# Route to get payment by ID
@app.get("/payments/{payment_id}", response_model=PaymentResponseModel)
async def get_payment_route(payment_id: int):
    async with get_session() as session:  # Explicitly creating session here
        payment = await get_payment_by_id(session, payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment

# Route to get all payments by user
@app.get("/users/{user_id}/payments", response_model=list[PaymentResponseModel])
async def get_user_payments(user_id: int):
    async with get_session() as session:  # Explicitly creating session here
        payments = await get_payments_by_user(session, user_id)
        if not payments:
            raise HTTPException(status_code=404, detail="No payments found for this user")
        return payments

# Route to update payment status
@app.put("/payments/{payment_id}/status")
async def update_payment_route(payment_id: int, new_status: str):
    async with get_session() as session:  # Explicitly creating session here
        payment = await update_payment_status(session, payment_id, new_status)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment

# Route to delete a payment
@app.delete("/payments/{payment_id}")
async def delete_payment_route(payment_id: int):
    async with get_session() as session:  # Explicitly creating session here
        payment = await delete_payment(session, payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return {"message": "Payment deleted successfully"}

# Route to refund a payment
@app.post("/refunds/")
async def refund_payment(payment_id: int, refund_amount: float, refund_reason: str):
    async with get_session() as session:  # Explicitly creating session here
        payment = await get_payment_by_id(session, payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        if payment.status == "refunded":
            raise HTTPException(status_code=400, detail="Payment has already been refunded")

        refund = await create_refund(payment_id=payment_id, refunded_amount=refund_amount, refund_reason=refund_reason, session=session)
        payment.status = "refunded"
        session.add(payment)
        await session.commit()
        await session.refresh(refund)

        return {
            "refund_id": refund.id,
            "payment_id": payment.id,
            "refunded_amount": refund.refunded_amount,
            "refund_reason": refund.refund_reason,
            "timestamp": refund.timestamp,
        }