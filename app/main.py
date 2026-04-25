from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.controllers.controller import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.validar()
    yield


app = FastAPI(
    title="Agente Mirim API",
    description="API de armazenamento de arquivos para o app Agente Mirim.",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def erro_generico(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Erro interno no servidor."})

app.include_router(router)

@app.get("/", include_in_schema=False)
async def root():
    return {"status": "online", "version": "2.0.0"}

@app.get("/health", tags=["Health"], summary="Health check")
async def health():
    return {"status": "ok"}
