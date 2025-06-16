from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from src.database import Base

class ChallengeCompletion(Base):
    __tablename__ = "challenge_completions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenge.id"), nullable=False)
    completed_at = Column(Date, nullable=False)

    user = relationship("User", back_populates="completed_challenges")
    challenge = relationship("Challenge", back_populates="completed_by")