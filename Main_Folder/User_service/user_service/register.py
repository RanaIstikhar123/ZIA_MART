from fastapi import HTTPException, Depends
from typing import Optional
from sqlalchemy.orm import Session
from user_service.models import User
from user_service.schemas import UserCreate, UserRead
from user_service.db import get_session
from user_service.auth import get_password_hash, get_user

# User registration
def register_user(user: UserCreate, db: Session = Depends(get_session)) -> UserRead:
  if user.email is None:  # Check if email is None
        raise HTTPException(status_code=400, detail="Email is required")
    
  db_user = get_user(db, email=user.email)
    
  if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
  hashed_password = get_password_hash(user.password)
  new_user = User(email=user.email, password=hashed_password)
    
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
    
  return UserRead.model_validate(new_user)
