from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import app.config as cfg
from app.controller import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    cfg.validar()
    yield


app = FastAPI(
    title="Agente Mirim — API de Arquivos",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def erro_generico(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Erro interno no servidor."})

app.include_router(router)

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
