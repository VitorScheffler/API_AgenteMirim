from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from app.controllers.controllers import router

app = FastAPI(
    title="Agente Mirim API",
    description="API de suporte ao aplicativo Agente Mirim — educação sobre prevenção de desastres naturais.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"], include_in_schema=False)
async def root():
    return {"status": "ok", "app": "Agente Mirim API", "version": "1.0.0"}

@app.get("/health", tags=["Health"], summary="Health check")
async def health():
    return {"status": "ok"}

app.include_router(router)
