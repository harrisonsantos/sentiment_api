"""
Aplicação principal FastAPI.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models import create_tables
from app.routes import router

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(router, prefix="/api/v1", tags=["reviews"])


@app.on_event("startup")
async def startup_event():
    """Evento executado na inicialização da aplicação."""
    create_tables()


@app.get("/")
async def root():
    """Endpoint raiz da API."""
    return {
        "message": "Sentiment Analysis API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
async def health_check():
    """Endpoint para verificação de saúde da API."""
    return {"status": "healthy", "message": "API está funcionando corretamente"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG
    )
