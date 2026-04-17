import uuid
from sqlalchemy import Column, String, Text, Integer, BigInteger, ForeignKey, TIMESTAMP
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


class Content(Base):
    """Conteúdo educativo exibido no app (textos, dicas, vídeos)."""
    __tablename__ = "contents"

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title       = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    category    = Column(String(50), nullable=False, default="geral")
    order_index = Column(Integer, nullable=False, default=0)
    file_id     = Column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="SET NULL"), nullable=True)
    created_at  = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at  = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)


class Mission(Base):
    """Missão educativa que o usuário pode completar no app."""
    __tablename__ = "missions"

    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title         = Column(Text, nullable=False)
    description   = Column(Text, nullable=False)
    difficulty    = Column(String(20), nullable=False, default="facil")  # facil | medio | dificil
    points        = Column(Integer, nullable=False, default=10)
    order_index   = Column(Integer, nullable=False, default=0)
    image_file_id = Column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="SET NULL"), nullable=True)
    created_at    = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at    = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)


class Medal(Base):
    """Medalha/conquista que o usuário pode desbloquear."""
    __tablename__ = "medals"

    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name          = Column(Text, nullable=False)
    description   = Column(Text, nullable=False)
    condition     = Column(Text, nullable=False)
    image_file_id = Column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="SET NULL"), nullable=True)
    created_at    = Column(TIMESTAMP, server_default=func.now(), nullable=False)
