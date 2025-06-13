"""
Schemas Pydantic para validação de dados.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    """Schema para criação de uma nova avaliação."""

    customer_name: str = Field(
        ..., min_length=1, max_length=255, description="Nome do cliente"
    )
    review_text: str = Field(..., min_length=1, description="Texto da avaliação")

    class Config:
        json_schema_extra = {
            "example": {
                "customer_name": "João Silva",
                "review_text": "Excelente atendimento, muito satisfeito com o serviço!",
            }
        }


class ReviewResponse(BaseModel):
    """Schema para resposta de uma avaliação."""

    id: int
    customer_name: str
    review_text: str
    sentiment: str
    confidence_score: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SentimentAnalysisResponse(BaseModel):
    """Schema para resposta da análise de sentimento."""

    id: int
    sentiment: str
    confidence_score: Optional[str] = None
    message: str = "Análise de sentimento realizada com sucesso"

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "sentiment": "positiva",
                "confidence_score": "0.85",
                "message": "Análise de sentimento realizada com sucesso",
            }
        }


class ReportResponse(BaseModel):
    """Schema para resposta do relatório de avaliações."""

    start_date: str
    end_date: str
    total_reviews: int
    positive_count: int
    negative_count: int
    neutral_count: int

    class Config:
        json_schema_extra = {
            "example": {
                "start_date": "2024-09-01",
                "end_date": "2024-09-17",
                "total_reviews": 10,
                "positive_count": 4,
                "negative_count": 3,
                "neutral_count": 3,
            }
        }
