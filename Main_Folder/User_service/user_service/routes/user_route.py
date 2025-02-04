from fastapi import APIRouter, Depends
from user_service.models import User
from user_service.schemas import UserRead
from user_service.auth import get_current_user

router = APIRouter()

@router.get("/user/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
