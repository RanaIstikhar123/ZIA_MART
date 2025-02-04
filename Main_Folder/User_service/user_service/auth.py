from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import Optional
from user_service.models import User
from user_service.schemas import Token, TokenData
from user_service.db import get_session
from user_service import settings
import os
from dotenv import load_dotenv
from starlette.config import Config
config = Config(".env")
load_dotenv()
# JWT Configuration
SECRET_KEY = config("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must not be None")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Hash password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Fetch user by email
def get_user(db: Session, email: str) -> Optional[User]:
    # Ensure email is not None before querying
    if email is None:
        return None
    return db.query(User).filter(User.email == email).first()   # type: ignore

# Authenticate user
def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user(db, email)
    if not user or not verify_password(password, user.password):
        return None
    return user

# Create JWT access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)    # type:ignore
    return encoded_jwt

from jose import JWTError, jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])   # type:ignore
        return payload  # Return the decoded token payload
    except JWTError:
        return None  # Invalid token
    

# Get the current user using JWT token
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # type:ignore
        email: Optional[str] = payload.get("sub")  # Email can be None
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = get_user(db, token_data.email)  # type: ignore
    if user is None:
        raise credentials_exception
    return user

# Function for login to get access token
async def login_for_access_token(form_data: OAuth2PasswordRequestForm, db: Session = Depends(get_session)) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")




