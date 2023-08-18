from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime




class Create_User(BaseModel):
    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    disabled: bool | None = None
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    disabled: bool | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str



class MessageBase(BaseModel):
    sending_to: str
    content: Optional[str] = None

class MessageCreate(MessageBase):
    pass

class MessageUpdate(MessageBase):
    pass

class MessageInDBBase(MessageBase):
    
    message_id: int
    created_at: str


