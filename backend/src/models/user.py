from sqlalchemy import Column, Integer, String, LargeBinary
from src.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(25), nullable=False, unique= False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    photo = Column(LargeBinary, nullable=True)
    bio = Column(String(255), nullable=True)