from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(25), nullable=False, unique= False)
    email = Column(String(255), nullable=False, unique=True)
    # email = Column(String(255), primary_key=True, index=True, unique=True)
    password = Column(String(255), nullable=False)
    photo = Column(String(255), nullable=True)
    profile = relationship("Profile", uselist=False, back_populates="user")