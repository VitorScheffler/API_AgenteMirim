import uuid
from sqlalchemy import Column, Text, BigInteger, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class File(Base):
    """Arquivo de mídia armazenado no sistema de arquivos local."""
    __tablename__ = "files"

    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename     = Column(Text, nullable=False)
    path         = Column(Text, nullable=False)
    content_type = Column(Text, nullable=False, default="application/octet-stream")
    size_bytes   = Column(BigInteger, nullable=False, default=0)
    created_at   = Column(TIMESTAMP, server_default=func.now(), nullable=False)
