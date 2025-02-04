from fastapi import HTTPException
from sqlmodel import Session, select
from notification_service.models import Notification
from datetime import datetime

# Create a new notification record
async def create_notification(user_id: int, message: str, event_type: str, session: Session):
    timestamp = datetime.now()
    notification = Notification(user_id=user_id, message=message, event_type=event_type, timestamp=timestamp)
    session.add(notification)
    await session.commit()
    await session.refresh(notification)
    return notification

# Retrieve notifications by user
async def get_notifications_by_user(user_id: int, session: Session):
    return session.exec(select(Notification).where(Notification.user_id == user_id)).all()

# Delete a notification
async def delete_notification(notification_id: int, session: Session):
    notification = session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    session.delete(notification)
    await session.commit()
    return {"message": f"Notification {notification_id} deleted successfully"}

# Update a notification
async def update_notification(notification_id: int, new_message: str, new_event_type: str, session: Session):
    notification = session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.message = new_message
    notification.event_type = new_event_type
    session.add(notification)
    await session.commit()
    await session.refresh(notification)
    return notification
