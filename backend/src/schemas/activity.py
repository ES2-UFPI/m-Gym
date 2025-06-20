from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ActivityCreate(BaseModel):
    challenge_id: int = Field(..., description="ID do desafio associado à atividade.")
    content: Optional[str] = Field(None, max_length=255, description="Texto da atividade (ex.: treino).")
    photo: Optional[str] = Field(None, description="Foto da atividade (base64).")
    comment: Optional[str] = Field(None, max_length=255, description="Comentário em outra atividade.")

class ActivityResponse(BaseModel):
    id: int
    user_id: int
    challenge_id: int
    content: Optional[str]
    photo: Optional[str]
    comment: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True