import os
import uuid

import aiofiles
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FastAPIFile, status
from fastapi.responses import FileResponse
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

import app.config as cfg
from app.database import get_db, File
from app.security import verify_token

router = APIRouter(
    prefix="/files",
    tags=["Arquivos"],
    dependencies=[Depends(verify_token)],
)


# ── Upload ────────────────────────────────────────────────────────────────────

@router.post("/upload", summary="Upload de arquivo")
async def upload(file: UploadFile = FastAPIFile(...), db: AsyncSession = Depends(get_db)):

    # Valida extensão
    if not file.filename or "." not in file.filename:
        raise HTTPException(status_code=400, detail="Arquivo sem extensão não permitido")

    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in cfg.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Extensão .{ext} não permitida")

    # Lê conteúdo
    conteudo = await file.read()
    if not conteudo:
        raise HTTPException(status_code=400, detail="Arquivo vazio")

    if cfg.MAX_UPLOAD_MB > 0 and len(conteudo) > cfg.MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail=f"Arquivo maior que {cfg.MAX_UPLOAD_MB}MB")

    # Salva no disco
    os.makedirs(cfg.UPLOAD_DIR, exist_ok=True)
    file_id  = uuid.uuid4()
    filename = f"{file_id}.{ext}"
    path     = os.path.join(cfg.UPLOAD_DIR, filename)

    async with aiofiles.open(path, "wb") as f:
        await f.write(conteudo)

    # Salva no banco — se falhar, remove do disco
    registro = File(
        id=file_id,
        filename=file.filename,
        path=path,
        content_type=file.content_type or "application/octet-stream",
        size_bytes=len(conteudo),
    )
    try:
        db.add(registro)
        await db.commit()
        await db.refresh(registro)
        return registro
    except Exception as e:
        os.remove(path)
        raise HTTPException(status_code=500, detail=f"Erro ao salvar no banco: {e}")


# ── Listar ────────────────────────────────────────────────────────────────────

@router.get("/", summary="Listar arquivos")
async def listar(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(File).order_by(File.created_at.desc()))
    return result.scalars().all()


# ── Download ──────────────────────────────────────────────────────────────────

@router.get("/{file_id}", summary="Download de arquivo")
async def download(file_id: str, db: AsyncSession = Depends(get_db)):
    f = await _buscar_ou_404(db, file_id)
    if not os.path.exists(f.path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado no disco")
    return FileResponse(path=f.path, filename=f.filename, media_type=f.content_type)


# ── Deletar ───────────────────────────────────────────────────────────────────

@router.delete("/{file_id}", summary="Remover arquivo")
async def deletar(file_id: str, db: AsyncSession = Depends(get_db)):
    f = await _buscar_ou_404(db, file_id)
    await db.execute(delete(File).where(File.id == f.id))
    await db.commit()
    if os.path.exists(f.path):
        os.remove(f.path)
    return {"detail": "Arquivo removido", "id": file_id}


# ── Helper ────────────────────────────────────────────────────────────────────

async def _buscar_ou_404(db: AsyncSession, file_id: str) -> File:
    try:
        fid = uuid.UUID(file_id)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"ID inválido: {file_id}")

    result = await db.execute(select(File).where(File.id == fid))
    f = result.scalar_one_or_none()
    if not f:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    return f
