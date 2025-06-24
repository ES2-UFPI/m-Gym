from datetime import date
from fastapi import FastAPI, HTTPException, Depends, Body, Form, status
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate, UserLogin, PerfilUpdate, AtualizaLoginRequest, AtualizaSenhaRequest, UserPoints
from src.schemas.challenge import ChallengeCreate, ChallengeResponse
from src.schemas.activity import ActivityCreate, ActivityResponse
from src.models.activity import Activity
from src.models.user import User
from src.models.challenge import Challenge
from src.database import get_db
from fastapi.middleware.cors import CORSMiddleware
from src.auth import authenticate_user, create_access_token, get_password_hash, get_current_user, verify_password
import base64
from pydantic import BaseModel
from typing import Optional
import os
from datetime import date
from src.models.challengecompletion import ChallengeCompletion
from src.models.challenge import Challenge
from src.models.user import User

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "https://m-gym.onrender.com", "https://mgymbackend.onrender.com/"],
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

@app.post("/desafios", status_code=201)
def criar_desafio(
    desafio: ChallengeCreate, 
    usuario_logado: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    
    novo_desafio = Challenge(
        title = desafio.title,
        description=desafio.description,
        start_date=desafio.start_date,
        end_date=desafio.end_date,
        points=desafio.points,
        creator_id=usuario_logado.id
    )
    if novo_desafio.start_date > novo_desafio.end_date:
        raise HTTPException(status_code=400, detail="A data de início deve ser anterior à data de término.")
    if novo_desafio.points < 0:
        raise HTTPException(status_code=400, detail="A quantidade de pontos deve ser um valor não negativo.")
    if novo_desafio.start_date < date.today():
        raise HTTPException(status_code=400, detail="A data de início não pode ser no passado.")
    
    db.add(novo_desafio)
    db.commit()
    db.refresh(novo_desafio)
    return {"message": "Desafio criado com sucesso!", "desafio": novo_desafio}

@app.get("/desafios", response_model=list[ChallengeResponse])
def listar_desafios(
    usuario_logado: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    desafios = db.query(Challenge).all()
    return desafios

@app.get("/usuarios/ranking", response_model=list[UserPoints])
def listar_ranking(db: Session = Depends(get_db)):
    usuarios = db.query(User).order_by(User.pontuacao.desc()).all()
    
    ranking = []
    for user in usuarios:
        ranking.append(UserPoints(
            login=user.login,
            email=user.email,
            photo=base64.b64encode(user.photo).decode('utf-8') if user.photo else None,
            points=user.pontuacao
        ))
    
    return ranking

@app.get("/desafios-ativos", response_model=list[ChallengeResponse])
def listar_desafios(
    usuario_logado: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    hoje = date.today()
    desafios = db.query(Challenge).filter(Challenge.start_date <= hoje, Challenge.end_date >= hoje).all()
    return desafios

@app.post("/desafios/{challenge_id}/participar")
def registrar_participacao(challenge_id: int,
                            usuario_logado: User = Depends(get_current_user),
                            db: Session = Depends(get_db)):

    desafio = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not desafio:
        raise HTTPException(status_code=404, detail="Desafio não encontrado")

    participacao_existente = db.query(ChallengeCompletion).filter_by(
        user_id=usuario_logado.id,
        challenge_id=challenge_id
    ).first()
    if participacao_existente:
        raise HTTPException(status_code=400, detail="Você já participou deste desafio")

    nova_participacao = ChallengeCompletion(
        user_id=usuario_logado.id,
        challenge_id=challenge_id,
        completed_at=date.today()
    )
    db.add(nova_participacao)

    # Atualiza a pontuação do usuário
    usuario_logado.pontuacao += desafio.points
    db.commit()

    return {"message": "Participação registrada com sucesso!", "pontos_ganhos": desafio.points}


@app.post("/atividades", response_model=ActivityResponse, status_code=201)
def criar_atividade(
    atividade: ActivityCreate,
    usuario_logado: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    nova_atividade = Activity(
        user_id=usuario_logado.id,
        challenge_id=atividade.challenge_id,
        content=atividade.content,
        photo=base64.b64decode(atividade.photo) if atividade.photo else None,
        comment=atividade.comment if atividade.comment else None
    )
    db.add(nova_atividade)
    db.commit()
    db.refresh(nova_atividade)
    return nova_atividade

@app.get("/atividades/{challenge_id}", response_model=list[ActivityResponse])
def listar_atividades(challenge_id: int, db: Session = Depends(get_db)):
    atividades = db.query(Activity).filter(Activity.challenge_id == challenge_id).all()
    return atividades

@app.get("/meus-desafios", response_model=list[ChallengeResponse])
def meus_desafios(
    usuario_logado: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Busca os desafios em que o usuário participou
    participacoes = db.query(ChallengeCompletion).filter_by(user_id=usuario_logado.id).all()
    desafios_ids = [p.challenge_id for p in participacoes]
    desafios = db.query(Challenge).filter(Challenge.id.in_(desafios_ids)).all()
    return desafios