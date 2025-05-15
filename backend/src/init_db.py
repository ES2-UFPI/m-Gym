from src.database import Base, engine
from src.models.user import User

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)
