"""
Testes unitários para as rotas da API.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models import Base, get_db

# Configurar banco de dados de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override da função get_db para usar banco de teste."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="function")
def setup_database():
    """Fixture para configurar banco de dados de teste."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestReviewsAPI:
    """Testes para as rotas da API de reviews."""

    def test_root_endpoint(self):
        """Testa endpoint raiz."""
        response = client.get("/")
        assert response.status_code == 200
        assert "Sentiment Analysis API" in response.json()["message"]

    def test_health_check(self):
        """Testa endpoint de health check."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_create_review(self, setup_database):
        """Testa criação de uma nova avaliação."""
        review_data = {
            "customer_name": "João Silva",
            "review_text": "Excelente atendimento, muito satisfeito!",
        }

        response = client.post("/api/v1/reviews", json=review_data)
        assert response.status_code == 201

        data = response.json()
        assert data["id"] is not None
        assert data["sentiment"] in ["positiva", "negativa", "neutra"]
        assert data["confidence_score"] is not None

    def test_get_all_reviews(self, setup_database):
        """Testa busca de todas as avaliações."""
        # Primeiro criar uma avaliação
        review_data = {
            "customer_name": "Maria Santos",
            "review_text": "Serviço regular, nada excepcional.",
        }
        client.post("/api/v1/reviews", json=review_data)

        # Buscar todas as avaliações
        response = client.get("/api/v1/reviews")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_review_by_id(self, setup_database):
        """Testa busca de avaliação por ID."""
        # Primeiro criar uma avaliação
        review_data = {
            "customer_name": "Pedro Costa",
            "review_text": "Péssimo atendimento, muito insatisfeito!",
        }
        create_response = client.post("/api/v1/reviews", json=review_data)
        review_id = create_response.json()["id"]

        # Buscar por ID
        response = client.get(f"/api/v1/reviews/{review_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == review_id
        assert data["customer_name"] == "Pedro Costa"

    def test_get_review_by_invalid_id(self, setup_database):
        """Testa busca de avaliação com ID inválido."""
        response = client.get("/api/v1/reviews/999")
        assert response.status_code == 404

    def test_get_reviews_report(self, setup_database):
        """Testa geração de relatório."""
        # Criar algumas avaliações
        reviews = [
            {"customer_name": "Ana", "review_text": "Ótimo serviço!"},
            {"customer_name": "Bruno", "review_text": "Péssimo atendimento!"},
            {"customer_name": "Carlos", "review_text": "Serviço ok."},
        ]

        for review in reviews:
            client.post("/api/v1/reviews", json=review)

        # Gerar relatório
        response = client.get(
            "/api/v1/reviews/report?start_date=2024-01-01&end_date=2024-12-31"
        )
        assert response.status_code == 200

        data = response.json()
        assert "total_reviews" in data
        assert "positive_count" in data
        assert "negative_count" in data
        assert "neutral_count" in data

    def test_get_reviews_report_invalid_date(self, setup_database):
        """Testa relatório com data inválida."""
        response = client.get(
            "/api/v1/reviews/report?start_date=invalid&end_date=2024-12-31"
        )
        assert response.status_code == 400
