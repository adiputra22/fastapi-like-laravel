from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class UserCreateRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    
    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v
    
    @field_validator('password')
    @classmethod
    def password_must_be_strong(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v

class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    
    class Config:
        from_attributes = True  # Untuk convert dari SQLAlchemy model