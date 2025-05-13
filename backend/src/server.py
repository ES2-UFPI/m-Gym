from fastapi import FastAPI, HTTPException
from src.schemas.user import UserCreate 
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ou ["*"] durante desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app_db = []

@app.post("/usuarios", status_code=201)
def criar_usuario(user: UserCreate):
    # Verifica se e-mail já está em uso
    for existing_user in app_db:
        if existing_user['email'] == user.email:
            raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    
    novo_usuario = user.dict()
    app_db.append(novo_usuario)
    return {"message": "Usuário criado com sucesso!", "usuario": novo_usuario}
