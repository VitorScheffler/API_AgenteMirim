"""
repositories.py — Repositórios para acesso ao banco de dados.
Cada repositório encapsula as queries da sua entidade.
"""
import uuid
from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import File, Content, Mission, Medal


# ── File Repository ───────────────────────────────────────────────────────────

class FileRepository:

    async def create(self, db: AsyncSession, file: File) -> File:
        db.add(file)
        await db.commit()
        await db.refresh(file)
        return file

    async def list_all(self, db: AsyncSession) -> List[File]:
        result = await db.execute(select(File).order_by(File.created_at.desc()))
        return list(result.scalars().all())

    async def get_by_id(self, db: AsyncSession, file_id: uuid.UUID) -> Optional[File]:
        result = await db.execute(select(File).where(File.id == file_id))
        return result.scalar_one_or_none()

    async def delete(self, db: AsyncSession, file_id: uuid.UUID) -> bool:
        result = await db.execute(delete(File).where(File.id == file_id))
        await db.commit()
        return result.rowcount > 0


# ── Content Repository ────────────────────────────────────────────────────────

class ContentRepository:

    async def create(self, db: AsyncSession, content: Content) -> Content:
        db.add(content)
        await db.commit()
        await db.refresh(content)
        return content

    async def list_all(self, db: AsyncSession, category: Optional[str] = None) -> List[Content]:
        query = select(Content).order_by(Content.order_index.asc())
        if category:
            query = query.where(Content.category == category)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, db: AsyncSession, content_id: uuid.UUID) -> Optional[Content]:
        result = await db.execute(select(Content).where(Content.id == content_id))
        return result.scalar_one_or_none()

    async def update(self, db: AsyncSession, content: Content, data: dict) -> Content:
        for key, value in data.items():
            if hasattr(content, key) and value is not None:
                setattr(content, key, value)
        await db.commit()
        await db.refresh(content)
        return content

    async def delete(self, db: AsyncSession, content_id: uuid.UUID) -> bool:
        result = await db.execute(delete(Content).where(Content.id == content_id))
        await db.commit()
        return result.rowcount > 0


# ── Mission Repository ────────────────────────────────────────────────────────

class MissionRepository:

    async def create(self, db: AsyncSession, mission: Mission) -> Mission:
        db.add(mission)
        await db.commit()
        await db.refresh(mission)
        return mission

    async def list_all(self, db: AsyncSession) -> List[Mission]:
        result = await db.execute(select(Mission).order_by(Mission.order_index.asc()))
        return list(result.scalars().all())

    async def get_by_id(self, db: AsyncSession, mission_id: uuid.UUID) -> Optional[Mission]:
        result = await db.execute(select(Mission).where(Mission.id == mission_id))
        return result.scalar_one_or_none()

    async def update(self, db: AsyncSession, mission: Mission, data: dict) -> Mission:
        for key, value in data.items():
            if hasattr(mission, key) and value is not None:
                setattr(mission, key, value)
        await db.commit()
        await db.refresh(mission)
        return mission

    async def delete(self, db: AsyncSession, mission_id: uuid.UUID) -> bool:
        result = await db.execute(delete(Mission).where(Mission.id == mission_id))
        await db.commit()
        return result.rowcount > 0


# ── Medal Repository ──────────────────────────────────────────────────────────

class MedalRepository:

    async def create(self, db: AsyncSession, medal: Medal) -> Medal:
        db.add(medal)
        await db.commit()
        await db.refresh(medal)
        return medal

    async def list_all(self, db: AsyncSession) -> List[Medal]:
        result = await db.execute(select(Medal).order_by(Medal.created_at.asc()))
        return list(result.scalars().all())

    async def get_by_id(self, db: AsyncSession, medal_id: uuid.UUID) -> Optional[Medal]:
        result = await db.execute(select(Medal).where(Medal.id == medal_id))
        return result.scalar_one_or_none()

    async def delete(self, db: AsyncSession, medal_id: uuid.UUID) -> bool:
        result = await db.execute(delete(Medal).where(Medal.id == medal_id))
        await db.commit()
        return result.rowcount > 0
