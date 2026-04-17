import os
import uuid
from fastapi import UploadFile, HTTPException
from app.models import File
from app.config import settings
from app.repositories.file_repository import FileRepository

repo = FileRepository()

class FileService:

    async def save_file(self, db, upload: UploadFile):
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

        file_id = uuid.uuid4()
        ext = upload.filename.split('.')[-1]
        filename = f"{file_id}.{ext}"
        path = os.path.join(settings.UPLOAD_DIR, filename)

        # salvar arquivo
        try:
            with open(path, "wb") as f:
                f.write(await upload.read())
        except Exception:
            raise HTTPException(500, "Erro ao salvar arquivo")

        file = File(
            id=file_id,
            filename=upload.filename,
            path=path
        )

        # salvar no banco
        try:
            await repo.create(db, file)
        except Exception:
            os.remove(path)  # rollback manual
            raise HTTPException(500, "Erro ao salvar no banco")

        return file

    async def list_files(self, db):
        return await repo.list_all(db)

    async def get_file(self, db, file_id):
        file = await repo.get_by_id(db, file_id)
        if not file:
            raise HTTPException(404, "Arquivo não encontrado")
        return file