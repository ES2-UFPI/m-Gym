from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import relationship
from src.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(25), nullable=False, unique=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    photo = Column(LargeBinary, nullable=True)
    bio = Column(String(255), nullable=True)
    pontuacao = Column(Integer, nullable=False, default=0)

    profile = relationship("Profile", uselist=False, back_populates="user")