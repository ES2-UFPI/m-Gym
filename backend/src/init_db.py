from src.database import Base, engine
from src.models import User, Profile, Challenge, ChallengeCompletion

Base.metadata.create_all(bind=engine)
