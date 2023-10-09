from pydantic import BaseModel, EmailStr
from typing import Optional

class ResetPasswordRequest(BaseModel):
    email: str


class ResetPasswordToken(BaseModel):
    token: str
    password: str

