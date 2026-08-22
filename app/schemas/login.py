from pydantic import BaseModel, Field
class loginSchema(BaseModel):
    username: str = Field(min_length=6)
    password: str = Field(min_length=6)
    email: str
