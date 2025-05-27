from src.database import Base, engine
from src.models import User, Profile

Base.metadata.create_all(bind=engine)
