import uuid
from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import File


class FileRepository:

    async def create(self, db: AsyncSession, file: File) -> File:
        db.add(file)
        await db.commit()
        await db.refresh(file)
        return file

    async def list_all(self, db: AsyncSession) -> List[File]:
        result = await db.execute(
            select(File).order_by(File.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, db: AsyncSession, file_id: uuid.UUID) -> Optional[File]:
        result = await db.execute(
            select(File).where(File.id == file_id)
        )
        return result.scalar_one_or_none()

    async def delete(self, db: AsyncSession, file_id: uuid.UUID) -> bool:
        result = await db.execute(
            delete(File).where(File.id == file_id)
        )
        await db.commit()
        return result.rowcount > 0
