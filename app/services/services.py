"""
services.py — Camada de serviço com toda a lógica de negócio.
"""
import os
import uuid
from typing import Optional, List

import aiofiles
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.models import File, Content, Mission, Medal
from app.repositories.repositories import (
    FileRepository, ContentRepository, MissionRepository, MedalRepository
)

file_repo    = FileRepository()
content_repo = ContentRepository()
mission_repo = MissionRepository()
medal_repo   = MedalRepository()


# ── FileService ───────────────────────────────────────────────────────────────

class FileService:

    async def upload(self, db: AsyncSession, upload: UploadFile) -> File:
        # Valida extensão
        ext = (upload.filename or "").rsplit(".", 1)[-1].lower()
        if ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de arquivo não permitido. Use: {', '.join(settings.ALLOWED_EXTENSIONS)}",
            )

        # Lê o conteúdo e valida tamanho
        content = await upload.read()
        if len(content) > settings.MAX_UPLOAD_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Arquivo maior que o limite de {settings.MAX_UPLOAD_MB}MB",
            )

        # Garante que o diretório existe
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

        file_id  = uuid.uuid4()
        filename = f"{file_id}.{ext}"
        path     = os.path.join(settings.UPLOAD_DIR, filename)

        # Salva no disco
        try:
            async with aiofiles.open(path, "wb") as f:
                await f.write(content)
        except OSError as e:
            raise HTTPException(status_code=500, detail=f"Erro ao salvar arquivo: {e}")

        # Salva no banco; se falhar, remove do disco (consistência)
        file = File(
            id=file_id,
            filename=upload.filename or filename,
            path=path,
            content_type=upload.content_type or "application/octet-stream",
            size_bytes=len(content),
        )
        try:
            return await file_repo.create(db, file)
        except Exception as e:
            if os.path.exists(path):
                os.remove(path)
            raise HTTPException(status_code=500, detail=f"Erro ao salvar no banco: {e}")

    async def list_files(self, db: AsyncSession) -> List[File]:
        return await file_repo.list_all(db)

    async def get_file(self, db: AsyncSession, file_id: str) -> File:
        try:
            fid = uuid.UUID(file_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID inválido")

        file = await file_repo.get_by_id(db, fid)
        if not file:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")
        if not os.path.exists(file.path):
            raise HTTPException(status_code=404, detail="Arquivo não encontrado no disco")
        return file

    async def delete_file(self, db: AsyncSession, file_id: str) -> dict:
        try:
            fid = uuid.UUID(file_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID inválido")

        file = await file_repo.get_by_id(db, fid)
        if not file:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")

        # Remove do banco primeiro
        await file_repo.delete(db, fid)

        # Remove do disco (ignora se não existir)
        if os.path.exists(file.path):
            os.remove(file.path)

        return {"detail": "Arquivo removido com sucesso"}


# ── ContentService ────────────────────────────────────────────────────────────

class ContentService:

    async def create(self, db: AsyncSession, data: dict) -> Content:
        content = Content(**data)
        return await content_repo.create(db, content)

    async def list_all(self, db: AsyncSession, category: Optional[str] = None) -> List[Content]:
        return await content_repo.list_all(db, category)

    async def get_by_id(self, db: AsyncSession, content_id: str) -> Content:
        try:
            cid = uuid.UUID(content_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID inválido")

        content = await content_repo.get_by_id(db, cid)
        if not content:
            raise HTTPException(status_code=404, detail="Conteúdo não encontrado")
        return content

    async def update(self, db: AsyncSession, content_id: str, data: dict) -> Content:
        content = await self.get_by_id(db, content_id)
        return await content_repo.update(db, content, data)

    async def delete(self, db: AsyncSession, content_id: str) -> dict:
        try:
            cid = uuid.UUID(content_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID inválido")

        deleted = await content_repo.delete(db, cid)
        if not deleted:
            raise HTTPException(status_code=404, detail="Conteúdo não encontrado")
        return {"detail": "Conteúdo removido com sucesso"}


# ── MissionService ────────────────────────────────────────────────────────────

class MissionService:

    async def create(self, db: AsyncSession, data: dict) -> Mission:
        mission = Mission(**data)
        return await mission_repo.create(db, mission)

    async def list_all(self, db: AsyncSession) -> List[Mission]:
        return await mission_repo.list_all(db)

    async def get_by_id(self, db: AsyncSession, mission_id: str) -> Mission:
        try:
            mid = uuid.UUID(mission_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID inválido")

        mission = await mission_repo.get_by_id(db, mid)
        if not mission:
            raise HTTPException(status_code=404, detail="Missão não encontrada")
        return mission

    async def update(self, db: AsyncSession, mission_id: str, data: dict) -> Mission:
        mission = await self.get_by_id(db, mission_id)
        return await mission_repo.update(db, mission, data)

    async def delete(self, db: AsyncSession, mission_id: str) -> dict:
        try:
            mid = uuid.UUID(mission_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID inválido")

        deleted = await mission_repo.delete(db, mid)
        if not deleted:
            raise HTTPException(status_code=404, detail="Missão não encontrada")
        return {"detail": "Missão removida com sucesso"}


# ── MedalService ──────────────────────────────────────────────────────────────

class MedalService:

    async def create(self, db: AsyncSession, data: dict) -> Medal:
        medal = Medal(**data)
        return await medal_repo.create(db, medal)

    async def list_all(self, db: AsyncSession) -> List[Medal]:
        return await medal_repo.list_all(db)

    async def get_by_id(self, db: AsyncSession, medal_id: str) -> Medal:
        try:
            mid = uuid.UUID(medal_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID inválido")

        medal = await medal_repo.get_by_id(db, mid)
        if not medal:
            raise HTTPException(status_code=404, detail="Medalha não encontrada")
        return medal

    async def delete(self, db: AsyncSession, medal_id: str) -> dict:
        try:
            mid = uuid.UUID(medal_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID inválido")

        deleted = await medal_repo.delete(db, mid)
        if not deleted:
            raise HTTPException(status_code=404, detail="Medalha não encontrada")
        return {"detail": "Medalha removida com sucesso"}
