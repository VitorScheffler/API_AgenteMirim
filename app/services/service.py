import os
import uuid
from typing import List

import aiofiles
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.models import File
from app.repositories.repository import FileRepository

repo = FileRepository()


class FileService:

    async def upload(self, db: AsyncSession, upload: UploadFile) -> File:
        # Valida se o arquivo tem nome
        if not upload.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nome do arquivo não informado",
            )

        # Valida extensão
        partes = upload.filename.rsplit(".", 1)
        if len(partes) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Arquivo sem extensão não é permitido",
            )
        ext = partes[-1].lower()
        if ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Extensão '.{ext}' não permitida. Use: {', '.join(sorted(settings.ALLOWED_EXTENSIONS))}",
            )

        # Lê conteúdo
        conteudo = await upload.read()
        if len(conteudo) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Arquivo vazio não é permitido",
            )

        # Valida tamanho (se limite configurado)
        if settings.MAX_UPLOAD_MB > 0 and len(conteudo) > settings.MAX_UPLOAD_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Arquivo maior que o limite de {settings.MAX_UPLOAD_MB}MB",
            )

        # Garante diretório de uploads
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

        file_id  = uuid.uuid4()
        filename = f"{file_id}.{ext}"
        path     = os.path.join(settings.UPLOAD_DIR, filename)

        # Salva no disco
        try:
            async with aiofiles.open(path, "wb") as f:
                await f.write(conteudo)
        except OSError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao salvar arquivo no disco: {e}",
            )

        # Salva metadados no banco — se falhar, remove do disco (consistência)
        file = File(
            id=file_id,
            filename=upload.filename,
            path=path,
            content_type=upload.content_type or "application/octet-stream",
            size_bytes=len(conteudo),
        )
        try:
            return await repo.create(db, file)
        except Exception as e:
            if os.path.exists(path):
                os.remove(path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao salvar metadados no banco: {e}",
            )

    async def list_files(self, db: AsyncSession) -> List[File]:
        return await repo.list_all(db)

    async def get_file(self, db: AsyncSession, file_id: str) -> File:
        fid = self._parse_uuid(file_id)
        file = await repo.get_by_id(db, fid)
        if not file:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Arquivo não encontrado")
        if not os.path.exists(file.path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Arquivo não encontrado no disco (registro órfão no banco)",
            )
        return file

    async def delete_file(self, db: AsyncSession, file_id: str) -> dict:
        fid  = self._parse_uuid(file_id)
        file = await repo.get_by_id(db, fid)
        if not file:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Arquivo não encontrado")

        # Remove do banco primeiro, depois do disco
        await repo.delete(db, fid)
        if os.path.exists(file.path):
            try:
                os.remove(file.path)
            except OSError:
                pass  # banco já removido — não bloqueia a resposta

        return {"detail": "Arquivo removido com sucesso", "id": file_id}

    @staticmethod
    def _parse_uuid(value: str) -> uuid.UUID:
        try:
            return uuid.UUID(value)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"ID inválido: '{value}' não é um UUID",
            )
