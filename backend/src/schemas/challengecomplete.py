from pydantic import BaseModel, Field
from datetime import date

class ChallengeCompletionCreate(BaseModel):
    challenge_id: int = Field(..., description="ID do desafio completado.")
    completed_at: date = Field(..., description="Data de conclusão do desafio.")

class ChallengeCompletionResponse(BaseModel):
    id: int
    user_id: int
    challenge_id: int
    completed_at: date

    class Config:
        orm_mode = True