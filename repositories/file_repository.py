from sqlalchemy.future import select
from app.models import File

class FileRepository:

    async def create(self, db, file):
        db.add(file)
        await db.commit()
        await db.refresh(file)
        return file

    async def list_all(self, db):
        result = await db.execute(select(File))
        return result.scalars().all()

    async def get_by_id(self, db, file_id):
        result = await db.execute(select(File).where(File.id == file_id))
        return result.scalar_one_or_none()