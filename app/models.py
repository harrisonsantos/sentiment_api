"""
Modelos de dados da aplicação.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

Base = declarative_base()


class Review(Base):
    """Modelo para armazenar avaliações e suas análises de sentimento."""

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False)
    review_text = Column(Text, nullable=False)
    sentiment = Column(String(50), nullable=False)  # positiva, negativa, neutra
    confidence_score = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return (
            f"<Review(id={self.id}, customer_name='{self.customer_name}', "
            f"sentiment='{self.sentiment}')>"
        )


# Configuração do banco de dados
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency para obter sessão do banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Cria as tabelas no banco de dados."""
    Base.metadata.create_all(bind=engine)
