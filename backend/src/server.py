from fastapi import FastAPI, HTTPException, Depends, Body, Form, status
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate, UserLogin
from src.models.user import User
from src.database import get_db
from fastapi.middleware.cors import CORSMiddleware
from src.auth import authenticate_user, create_access_token, get_password_hash

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/usuarios", status_code=201)
def criar_usuario(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    
    novo_usuario = User(
        login=user.login,
        email=user.email,
        password=get_password_hash(user.password),
        photo=user.photo
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return {"message": "Usuário criado com sucesso!", "usuario": novo_usuario}

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}