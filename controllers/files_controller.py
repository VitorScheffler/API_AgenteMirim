from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from app.database import AsyncSessionLocal
from app.services.file_service import FileService
from app.utils.security import verify_token

router = APIRouter()
service = FileService()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/upload", dependencies=[Depends(verify_token)])
async def upload_file(file: UploadFile, db=Depends(get_db)):
    return await service.save_file(db, file)

@router.get("/files", dependencies=[Depends(verify_token)])
async def list_files(db=Depends(get_db)):
    return await service.list_files(db)

@router.get("/files/{file_id}", dependencies=[Depends(verify_token)])
async def download_file(file_id: str, db=Depends(get_db)):
    file = await service.get_file(db, file_id)
    return FileResponse(file.path, filename=file.filename)