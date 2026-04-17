"""
controllers.py — Rotas da API (Controllers).
Recebe as requisições, chama os services e retorna as respostas.
"""
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile
from fastapi.responses import FileResponse

from app.database import get_db
from app.utils.security import verify_token
from app.services.services import FileService, ContentService, MissionService, MedalService

# Instâncias dos services
file_service    = FileService()
content_service = ContentService()
mission_service = MissionService()
medal_service   = MedalService()

router = APIRouter(dependencies=[Depends(verify_token)])


# ── Arquivos ──────────────────────────────────────────────────────────────────

@router.post("/upload", tags=["Arquivos"], summary="Faz upload de um arquivo de mídia")
async def upload_file(
    file: UploadFile = FastAPIFile(..., description="Arquivo a ser enviado"),
    db=Depends(get_db),
):
    return await file_service.upload(db, file)


@router.get("/files", tags=["Arquivos"], summary="Lista todos os arquivos")
async def list_files(db=Depends(get_db)):
    return await file_service.list_files(db)


@router.get("/files/{file_id}", tags=["Arquivos"], summary="Download de um arquivo pelo ID")
async def download_file(file_id: str, db=Depends(get_db)):
    file = await file_service.get_file(db, file_id)
    return FileResponse(file.path, filename=file.filename, media_type=file.content_type)


@router.delete("/files/{file_id}", tags=["Arquivos"], summary="Remove um arquivo")
async def delete_file(file_id: str, db=Depends(get_db)):
    return await file_service.delete_file(db, file_id)


# ── Conteúdos ─────────────────────────────────────────────────────────────────

@router.get("/contents", tags=["Conteúdos"], summary="Lista conteúdos educativos")
async def list_contents(
    category: Optional[str] = None,
    db=Depends(get_db),
):
    """
    Retorna os conteúdos ordenados por `order_index`.
    Filtre por categoria: enchentes | deslizamentos | tempestades | preparacao | geral
    """
    return await content_service.list_all(db, category)


@router.get("/contents/{content_id}", tags=["Conteúdos"], summary="Detalhe de um conteúdo")
async def get_content(content_id: str, db=Depends(get_db)):
    return await content_service.get_by_id(db, content_id)


@router.post("/contents", tags=["Conteúdos"], summary="Cria um novo conteúdo")
async def create_content(body: dict, db=Depends(get_db)):
    """
    Campos esperados:
    - title (str, obrigatório)
    - description (str, obrigatório)
    - category (str): enchentes | deslizamentos | tempestades | preparacao | geral
    - order_index (int): posição na lista
    - file_id (uuid, opcional): ID de um arquivo já carregado via /upload
    """
    return await content_service.create(db, body)


@router.put("/contents/{content_id}", tags=["Conteúdos"], summary="Atualiza um conteúdo")
async def update_content(content_id: str, body: dict, db=Depends(get_db)):
    return await content_service.update(db, content_id, body)


@router.delete("/contents/{content_id}", tags=["Conteúdos"], summary="Remove um conteúdo")
async def delete_content(content_id: str, db=Depends(get_db)):
    return await content_service.delete(db, content_id)


# ── Missões ───────────────────────────────────────────────────────────────────

@router.get("/missions", tags=["Missões"], summary="Lista missões educativas")
async def list_missions(db=Depends(get_db)):
    """Retorna as missões ordenadas por dificuldade/ordem."""
    return await mission_service.list_all(db)


@router.get("/missions/{mission_id}", tags=["Missões"], summary="Detalhe de uma missão")
async def get_mission(mission_id: str, db=Depends(get_db)):
    return await mission_service.get_by_id(db, mission_id)


@router.post("/missions", tags=["Missões"], summary="Cria uma nova missão")
async def create_mission(body: dict, db=Depends(get_db)):
    """
    Campos esperados:
    - title (str, obrigatório)
    - description (str, obrigatório)
    - difficulty (str): facil | medio | dificil
    - points (int): pontos ao completar
    - order_index (int): posição na lista
    - image_file_id (uuid, opcional)
    """
    return await mission_service.create(db, body)


@router.put("/missions/{mission_id}", tags=["Missões"], summary="Atualiza uma missão")
async def update_mission(mission_id: str, body: dict, db=Depends(get_db)):
    return await mission_service.update(db, mission_id, body)


@router.delete("/missions/{mission_id}", tags=["Missões"], summary="Remove uma missão")
async def delete_mission(mission_id: str, db=Depends(get_db)):
    return await mission_service.delete(db, mission_id)


# ── Medalhas ──────────────────────────────────────────────────────────────────

@router.get("/medals", tags=["Medalhas"], summary="Lista medalhas/conquistas")
async def list_medals(db=Depends(get_db)):
    return await medal_service.list_all(db)


@router.get("/medals/{medal_id}", tags=["Medalhas"], summary="Detalhe de uma medalha")
async def get_medal(medal_id: str, db=Depends(get_db)):
    return await medal_service.get_by_id(db, medal_id)


@router.post("/medals", tags=["Medalhas"], summary="Cria uma nova medalha")
async def create_medal(body: dict, db=Depends(get_db)):
    """
    Campos esperados:
    - name (str, obrigatório)
    - description (str, obrigatório)
    - condition (str, obrigatório): critério para desbloquear
    - image_file_id (uuid, opcional)
    """
    return await medal_service.create(db, body)


@router.delete("/medals/{medal_id}", tags=["Medalhas"], summary="Remove uma medalha")
async def delete_medal(medal_id: str, db=Depends(get_db)):
    return await medal_service.delete(db, medal_id)
