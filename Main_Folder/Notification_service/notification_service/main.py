from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

from sqlmodel import Session
from notification_service.crud import delete_notification, get_notifications_by_user, update_notification
from notification_service.kafka_utils import consume_order_messages, consume_payment_messages
from notification_service.db import create_db_and_tables, get_session
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

# Async lifespan for handling startup and shutdown processes
@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Creating Database Tables...")
    await create_db_and_tables()

    # Start Kafka consumers for both order and payment messages
    asyncio.create_task(consume_order_messages())
    asyncio.create_task(consume_payment_messages())

    yield

# Initialize FastAPI app with lifespan management
app = FastAPI(
    lifespan=lifespan,
    title="Notification Service",
    version="0.1"
)

@app.get("/")
def read_root():
    return {"Hello": "Notification Service"}
# API Routes for notifications
@app.get("/notifications/{user_id}")
async def get_user_notifications(user_id: int, session: Session = Depends(get_session)):
    notifications = await get_notifications_by_user(user_id, session)
    if not notifications:
        return {"message": "No notifications found for this user"}
    return {"notifications": notifications}

@app.delete("/notifications/{notification_id}")
async def delete_user_notification(notification_id: int, session: Session = Depends(get_session)):
    return await delete_notification(notification_id, session)

@app.put("/notifications/{notification_id}")
async def update_user_notification(notification_id: int, new_message: str, new_event_type: str, session: Session = Depends(get_session)):
    return await update_notification(notification_id, new_message, new_event_type, session)

@app.get("/health")
def health_check():
    return {"status": "Notification Service is running"}
