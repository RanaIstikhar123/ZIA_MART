from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from user_service.schemas import UserCreate, UserRead
from user_service.register import register_user
from user_service.db import get_session


router = APIRouter()

# Route for user registration
@router.post("/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_session)):
    return register_user(user, db)
