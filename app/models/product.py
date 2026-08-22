from app.database.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True, nullable=False)

    description = Column(String, nullable=False)

    price = Column(Float, nullable=False)

    category = Column(String, nullable=False)

    stock = Column(Integer, nullable=True, default=0)

    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )