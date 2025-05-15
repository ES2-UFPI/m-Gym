from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate
from src.models.user import User
from src.database import get_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],  # ou ["*"] durante desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/usuarios", status_code=201)
def criar_usuario(user: UserCreate, db: Session = Depends(get_db)):
    # Verifica se o e-mail já está em uso
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    
    
    # Cria um novo usuário
    novo_usuario = User(
        login=user.login,
        email=user.email,
        password=user.password,  # Certifique-se de usar hash para senhas
        photo=user.photo
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return {"message": "Usuário criado com sucesso!", "usuario": novo_usuario}
