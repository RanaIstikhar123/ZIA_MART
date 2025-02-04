from pydantic import BaseModel
from typing import Optional

# Schema for creating a user
class UserCreate(BaseModel):
    email : Optional[str]
    password: str

# Schema for reading user data
class UserRead(BaseModel):
    id: Optional[int]
    email: Optional[str]
    class Config:
        from_attributes = True
# JWT Token schema
class Token(BaseModel):
    access_token: str
    token_type: str

# Token data for JWT validation
class TokenData(BaseModel):
    email: Optional[str] = None
