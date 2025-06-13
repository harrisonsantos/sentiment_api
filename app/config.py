"""
Configurações da aplicação.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Configurações da aplicação."""
    
    # Configurações do banco de dados
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@localhost:5432/sentiment_db"
    )
    
    # Configurações da API
    API_TITLE: str = "Sentiment Analysis API"
    API_DESCRIPTION: str = "API para análise de sentimento de avaliações de clientes"
    API_VERSION: str = "1.0.0"
    
    # Configurações do servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Configurações do Groq LLM
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "gsk_YOUR_GROQ_API_KEY")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    # Configurações de análise de sentimento
    USE_LLM_ANALYSIS: bool = os.getenv("USE_LLM_ANALYSIS", "True").lower() == "true"
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "1024"))
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.1"))


settings = Settings()