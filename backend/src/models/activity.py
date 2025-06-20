from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenge.id"), nullable=False)
    content = Column(String(255), nullable=True)  # Texto da atividade (ex.: treino)
    photo = Column(LargeBinary, nullable=True)  # Foto opcional
    comment = Column(String(255), nullable=True)  # Comentário opcional
    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp da atividade

    # Relacionamentos
    user = relationship("User", back_populates="activities")
    challenge = relationship("Challenge", back_populates="activities")