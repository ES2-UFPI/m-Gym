from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from src.database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, ForeignKey("users.id"), index=True)
    login = Column(Integer, nullable=False, index=True)
    bio = Column(String(255), nullable=True)
    photo = Column(LargeBinary, nullable=True)

    user = relationship("User", back_populates="profile")