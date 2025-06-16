from pydantic import BaseModel, Field
from datetime import date

class ChallengeCreate(BaseModel):
    title: str = Field(..., max_length=255, description="Título do desafio.")
    description: str = Field(..., max_length=255, description="Descrição do desafio.")
    start_date: date = Field(..., description="Data de início do desafio.")
    end_date: date = Field(..., description="Data de término do desafio.")
    points: int = Field(..., ge=0, description="Quantidade de pontos que o desafio vale.")

class ChallengeResponse(BaseModel):
    id: int
    title: str
    description: str
    start_date: date
    end_date: date
    points: int
    creator_id: int

    class Config:
        orm_mode = True