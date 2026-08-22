from pydantic import BaseModel


class ProductCreateSchema(BaseModel):
    name: str
    description: str
    price: float
    category: str
    stock: int
    is_active: bool