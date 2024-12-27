from pydantic import BaseModel, EmailStr
from typing import Optional

# Base class for User-related schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str

# Class for user creation, extending UserBase
class UserCreate(UserBase):
    password: str

# Class for output when retrieving user data
class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

# Class for login response, to return the access token and token type
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"  # The token type is usually "bearer"

    class Config:
        orm_mode = True

# Class for login request, to get the email and password
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    password: Optional[str] = None