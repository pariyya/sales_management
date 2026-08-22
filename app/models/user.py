from app.database.database import Base
from sqlalchemy import Column,INTEGER,String
class User(Base):
    __tablename__ = "users"
    id = Column(INTEGER, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String,unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="USER")