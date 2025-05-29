from pydantic import BaseModel, EmailStr
from datetime import datetime

# Schema for user creation (register)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Schema for user response (what the API returns)
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode for SQLAlchemy

# Schema for login request
class UserLogin(BaseModel):
    username: str
    # email: EmailStr
    password: str

# Schema for token response
class Token(BaseModel):
    access_token: str
    token_type: str