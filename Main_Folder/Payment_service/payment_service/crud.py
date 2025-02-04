import logging
logging.basicConfig(level=logging.INFO)
from sqlmodel import Session, select
from payment_service.models import Payment, Refund
from datetime import datetime

# Create a new payment record
async def create_payment(session: Session, order_id: int, user_id: int, total_amount: float, status: str):
    try:
        logging.info(f"Attempting to create payment for order_id={order_id}, user_id={user_id}, total_amount={total_amount}")
        payment = Payment(order_id=order_id, user_id=user_id, total_amount=total_amount, status=status)
        session.add(payment)
        logging.info("Payment added to session, attempting commit")
        await session.commit()
        logging.info("Payment committed to database")
        await session.refresh(payment)
        logging.info(f"Payment refreshed: {payment}")
        return payment
    except Exception as e:
        logging.error(f"Error during payment creation: {e}")
        raise


# Get a payment by ID
# Get all payments for a specific user
async def get_payments_by_user(session: Session, user_id: int):
    result = await session.execute(select(Payment).where(Payment.user_id == user_id))
    return result.scalars().all()
from sqlmodel import Session, select
from payment_service.models import Payment, Refund
from datetime import datetime

# Get a payment by ID
async def get_payment_by_id(session: Session, payment_id: int):
    result = await session.execute(select(Payment).where(Payment.id == payment_id))
    return result.scalar_one_or_none()

# Get all payments for a user
async def get_payments_by_user(session: Session, user_id: int):
    result = await session.execute(select(Payment).where(Payment.user_id == user_id))
    return result.scalars().all()

# Update a payment status
async def update_payment_status(session: Session, payment_id: int, new_status: str):
    payment = await get_payment_by_id(session, payment_id)
    if payment:
        payment.status = new_status
        await session.commit()
        await session.refresh(payment)
    return payment

# Delete a payment record
async def delete_payment(session: Session, payment_id: int):
    payment = await get_payment_by_id(session, payment_id)
    if payment:
        await session.delete(payment)
        await session.commit()
    return payment

# Create a new refund
async def create_refund(payment_id: int, refunded_amount: float, refund_reason: str, session: Session):
    # Ensure the payment exists before issuing a refund
    payment = await get_payment_by_id(session, payment_id)
    if not payment:
        raise ValueError("Payment not found. Cannot create refund.")

    # Create a new refund record
    refund = Refund(payment_id=payment.id, refunded_amount=refunded_amount, refund_reason=refund_reason)
    session.add(refund)
    await session.commit()
    await session.refresh(refund)
    
    # Optionally, update payment status to refunded
    payment.status = "refunded"
    session.add(payment)
    await session.commit()

    return refund
