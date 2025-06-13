"""
Rotas da API para análise de sentimento.
"""
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models import Review, get_db
from app.schemas import (
    ReviewCreate,
    ReviewResponse,
    SentimentAnalysisResponse,
    ReportResponse,
)
from app.sentiment_service import SentimentAnalyzer

router = APIRouter()
sentiment_analyzer = SentimentAnalyzer()


@router.post("/reviews", response_model=SentimentAnalysisResponse, status_code=201)
async def create_review(review_data: ReviewCreate, db: Session = Depends(get_db)):
    """
    Classifica uma avaliação de cliente usando análise de sentimento.

    Args:
        review_data (ReviewCreate): Dados da avaliação
        db (Session): Sessão do banco de dados

    Returns:
        SentimentAnalysisResponse: Resultado da análise de sentimento
    """
    try:
        # Realizar análise de sentimento
        sentiment, confidence_score = sentiment_analyzer.analyze_sentiment(
            review_data.review_text
        )

        # Criar nova avaliação no banco
        db_review = Review(
            customer_name=review_data.customer_name,
            review_text=review_data.review_text,
            sentiment=sentiment,
            confidence_score=confidence_score,
        )

        db.add(db_review)
        db.commit()
        db.refresh(db_review)

        return SentimentAnalysisResponse(
            id=db_review.id,
            sentiment=sentiment,
            confidence_score=confidence_score,
            message="Análise de sentimento realizada com sucesso",
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}"
        )


@router.get("/reviews", response_model=List[ReviewResponse])
async def get_all_reviews(
    skip: int = Query(0, ge=0, description="Número de registros a pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    db: Session = Depends(get_db),
):
    """
    Retorna uma lista de todas as avaliações analisadas.

    Args:
        skip (int): Número de registros a pular (paginação)
        limit (int): Número máximo de registros a retornar
        db (Session): Sessão do banco de dados

    Returns:
        List[ReviewResponse]: Lista de avaliações
    """
    try:
        reviews = db.query(Review).offset(skip).limit(limit).all()
        return reviews

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao buscar avaliações: {str(e)}"
        )


@router.get("/reviews/report", response_model=ReportResponse)
async def get_reviews_report(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    """
    Retorna um relatório das avaliações em um período específico.

    Args:
        start_date (str): Data inicial no formato YYYY-MM-DD
        end_date (str): Data final no formato YYYY-MM-DD
        db (Session): Sessão do banco de dados

    Returns:
        ReportResponse: Relatório com contagem de sentimentos
    """
    try:
        # Validar formato das datas
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD"
            )

        # Verificar se data inicial é menor que final
        if start_dt > end_dt:
            raise HTTPException(
                status_code=400,
                detail="Data inicial deve ser menor ou igual à data final",
            )

        # Buscar avaliações no período
        reviews = (
            db.query(Review)
            .filter(
                and_(
                    Review.created_at >= start_dt,
                    Review.created_at <= end_dt.replace(hour=23, minute=59, second=59),
                )
            )
            .all()
        )

        # Contar sentimentos
        total_reviews = len(reviews)
        positive_count = len([r for r in reviews if r.sentiment == "positiva"])
        negative_count = len([r for r in reviews if r.sentiment == "negativa"])
        neutral_count = len([r for r in reviews if r.sentiment == "neutra"])

        return ReportResponse(
            start_date=start_date,
            end_date=end_date,
            total_reviews=total_reviews,
            positive_count=positive_count,
            negative_count=negative_count,
            neutral_count=neutral_count,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao gerar relatório: {str(e)}"
        )


@router.get("/reviews/{review_id}", response_model=ReviewResponse)
async def get_review_by_id(review_id: int, db: Session = Depends(get_db)):
    """
    Busca uma avaliação específica pelo ID.

    Args:
        review_id (int): ID da avaliação
        db (Session): Sessão do banco de dados

    Returns:
        ReviewResponse: Dados da avaliação
    """
    try:
        review = db.query(Review).filter(Review.id == review_id).first()

        if not review:
            raise HTTPException(
                status_code=404, detail=f"Avaliação com ID {review_id} não encontrada"
            )

        return review

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao buscar avaliação: {str(e)}"
        )
