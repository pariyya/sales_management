from sqlalchemy import Column, Integer, Float, String, DateTime
from app.database.database import Base
from datetime import datetime


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)

    customer_id = Column(Integer, nullable=False)

    total_price = Column(Float, nullable=False, default=0)

    status = Column(String, nullable=False, default="PENDING")

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)