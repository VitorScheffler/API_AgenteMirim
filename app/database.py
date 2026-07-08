import uuid
from sqlalchemy import Column, Text, BigInteger, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

import app.config as cfg

engine = create_async_engine(cfg.DB_URL, echo=False, pool_pre_ping=True)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()


# ── Único model do sistema ────────────────────────────────────────────────────

class File(Base):
    __tablename__ = "files"

    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename     = Column(Text, nullable=False)
    path         = Column(Text, nullable=False)
    content_type = Column(Text, nullable=False, default="application/octet-stream")
    size_bytes   = Column(BigInteger, nullable=False, default=0)
    created_at   = Column(TIMESTAMP, server_default=func.now(), nullable=False)


# ── Dependency do FastAPI ─────────────────────────────────────────────────────

async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
