from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from user_service.auth import login_for_access_token
from user_service.db import get_session
from user_service.schemas import Token

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    return await login_for_access_token(form_data, db)

