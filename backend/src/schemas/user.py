from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    login: str = Field(..., max_length=25, description="Login do usuário, obrigatório e com até 25 caracteres.")
    email: EmailStr = Field(..., description="Email único e válido do usuário.")
    password: str = Field(..., min_length=6, description="Senha do usuário, obrigatória e com no mínimo 6 caracteres.")
    photo: str = Field(None, description="URL da foto do usuário, opcional.")