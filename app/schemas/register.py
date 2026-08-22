#this module handles user registration imput data
#define the required fields that each user must has it for register
#validate user information before registration
from pydantic import BaseModel
from typing import Optional

class RegisterSchema(BaseModel):
    username: str
    password: str
    email: str
    admin_key: Optional[str] = None