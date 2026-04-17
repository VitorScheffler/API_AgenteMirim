"""
main.py — Entry point da API Agente Mirim.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.controllers import router

app = FastAPI(
    title="Agente Mirim API",
    description=(
        "API de suporte ao aplicativo Agente Mirim — "
        "educação sobre prevenção de desastres naturais. "
        "Gerencia arquivos de mídia, conteúdos, missões e medalhas."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — ajuste as origens conforme necessário para produção
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["Health"], summary="Health check")
async def root():
    return {"status": "ok", "app": "Agente Mirim API", "version": "1.0.0"}
