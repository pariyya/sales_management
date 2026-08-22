from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app.database.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    phone = Column(String, nullable=False)

    email = Column(String, nullable=False)

    address = Column(String, nullable=False)

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )