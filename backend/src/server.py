from fastapi import FastAPI, HTTPException, Depends, Body, Form, status
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate, UserLogin, PerfilUpdate, AtualizaLoginRequest, AtualizaSenhaRequest
from src.models.user import User
from src.database import get_db
from fastapi.middleware.cors import CORSMiddleware
from src.auth import authenticate_user, create_access_token, get_password_hash, get_current_user, verify_password
import base64
from pydantic import BaseModel
from typing import Optional

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
def login(user: UserLogin, db: Session = Depends(get_db)):
    user_autenticado = authenticate_user(db, user.email, user.password)
    if not user_autenticado:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    token = create_access_token({"sub": user_autenticado.email})

    photo_base64 = (
        base64.b64encode(user_autenticado.photo).decode('utf-8')
        if user_autenticado.photo else None
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "id": user_autenticado.id,
            "login": user_autenticado.login,
            "email": user_autenticado.email,
            "bio": user_autenticado.bio,
            "photo": photo_base64,
            "pontuacao": user_autenticado.pontuacao,
        }
    }

@app.get("/perfil")
def perfil(usuario=Depends(get_current_user)):
    photo_base64 = (
        base64.b64encode(usuario.photo).decode('utf-8')
        if usuario.photo else None
    )
    return {
        "usuario": usuario.login,
        "email": usuario.email,
        "photo": photo_base64,  
        "bio": usuario.bio,
        "pontuacao": usuario.pontuacao
    }

@app.put("/perfil")
def atualiza_perfil(perfil: PerfilUpdate, 
                  usuario_logado: User = Depends(get_current_user), 
                  db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.id == usuario_logado.id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if perfil.photo:
        try:
            usuario.photo = base64.b64decode(perfil.photo)
        except Exception:
            raise HTTPException(status_code=400, detail="Foto inválida")

    if perfil.bio is not None:
        usuario.bio = perfil.bio
    
    db.commit()
    db.refresh(usuario)
    return {"usuario": {
        "login": usuario.login,
        "email": usuario.email,
        "photo": perfil.photo,  # retorna base64 para o frontend
        "bio": usuario.bio,
        "pontuacao": usuario.pontuacao
    }}

@app.put("/usuarios/atualizar-login")
def atualizar_login(
    dados: AtualizaLoginRequest,
    usuario_logado: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if db.query(User).filter(User.login == dados.novo_login).first():
        raise HTTPException(status_code=400, detail="Login já está em uso.")

    usuario_logado.login = dados.novo_login
    db.commit()
    return {"message": "Login atualizado com sucesso."}

@app.put("/usuarios/atualizar-senha")
async def atualizar_senha(
    dados: AtualizaSenhaRequest,
    usuario_logado: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(dados.senha_antiga, usuario_logado.password):
        raise HTTPException(status_code=401, detail="Senha antiga incorreta.")
    
    # user = user.db.query(User).filter(User.id == usuario_logado.id)
    usuario_logado.password = get_password_hash(dados.nova_senha)
    db.add(usuario_logado)  
    db.commit()
    db.refresh(usuario_logado) 

    return {"message": "Senha atualizada com sucesso."}

