from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile
from fastapi.responses import FileResponse

from app.database import get_db
from app.utils.security import verify_token
from app.services.service import FileService

service = FileService()
router  = APIRouter(
    prefix="/files",
    tags=["📁 Arquivos"],
    dependencies=[Depends(verify_token)],
)


@router.post(
    "/upload",
    summary="Upload de arquivo",
    description="Envia um arquivo (imagem, vídeo ou PDF) e salva no servidor. Retorna os metadados.",
)
async def upload_file(
    file: UploadFile = FastAPIFile(..., description="Arquivo a enviar"),
    db=Depends(get_db),
):
    return await service.upload(db, file)


@router.get(
    "/",
    summary="Listar arquivos",
    description="Retorna todos os arquivos cadastrados, do mais recente para o mais antigo.",
)
async def list_files(db=Depends(get_db)):
    return await service.list_files(db)


@router.get(
    "/{file_id}",
    summary="Download de arquivo",
    description="Faz o download do arquivo pelo ID (UUID). Retorna o arquivo binário.",
)
async def download_file(file_id: str, db=Depends(get_db)):
    file = await service.get_file(db, file_id)
    return FileResponse(
        path=file.path,
        filename=file.filename,
        media_type=file.content_type,
    )


@router.delete(
    "/{file_id}",
    summary="Remover arquivo",
    description="Remove o arquivo do banco de dados e do disco permanentemente.",
)
async def delete_file(file_id: str, db=Depends(get_db)):
    return await service.delete_file(db, file_id)
