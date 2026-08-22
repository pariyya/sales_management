from pydantic import BaseModel


class CustomerSchema(BaseModel):
    name: str
    phone: str
    email: str
    address: str