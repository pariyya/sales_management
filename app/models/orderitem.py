from sqlalchemy import Column, Integer, Float
from app.database.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)

    order_id = Column(Integer, nullable=False)

    product_id = Column(Integer, nullable=False)

    quantity = Column(Integer, nullable=False)

    unit_price = Column(Float, nullable=False)

    total_price = Column(Float, nullable=False)