from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    login: str = Field(..., max_length=25, description="Login do usuário, obrigatório e com até 25 caracteres.")
    email: EmailStr = Field(..., description="Email único e válido do usuário.")
    password: str = Field(..., min_length=6, description="Senha do usuário, obrigatória e com no mínimo 6 caracteres.")
    photo: Optional[str] = Field(None, description="foto do usuário, opcional.")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Email único e válido do usuário.")
    password: str = Field(..., min_length=6, description="Senha do usuário, obrigatória e com no mínimo 6 caracteres.")

class UserResponse(BaseModel):
    id: int
    login: str
    email: EmailStr
    photo: Optional[str] = None

    class Config:
        orm_mode = True

class PerfilUpdate(BaseModel):
    bio: Optional[str] = None
    photo: Optional[str] = None 

class AtualizaLoginRequest(BaseModel):
    novo_login: str

class AtualizaSenhaRequest(BaseModel):
    senha_antiga: str
    nova_senha: str =  Field(..., min_length=6, description="Senha do usuário, obrigatória e com no mínimo 6 caracteres.")