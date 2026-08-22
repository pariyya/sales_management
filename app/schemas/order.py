from pydantic import BaseModel


class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int


class OrderSchema(BaseModel):
    customer_id: int
    items: list[OrderItemSchema]