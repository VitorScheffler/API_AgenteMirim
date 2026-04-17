import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Banco de dados
    DB_HOST:     str = os.getenv("DB_HOST", "localhost")
    DB_PORT:     str = os.getenv("DB_PORT", "5432")
    DB_NAME:     str = os.getenv("DB_NAME", "agentemirim_db")
    DB_USER:     str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")

    @property
    def DB_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # Storage
    UPLOAD_DIR:    str = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_UPLOAD_MB: int = int(os.getenv("MAX_UPLOAD_MB", "10"))

    @property
    def MAX_UPLOAD_BYTES(self) -> int:
        return self.MAX_UPLOAD_MB * 1024 * 1024

    # Tipos de arquivo permitidos
    ALLOWED_EXTENSIONS: set = {"jpg", "jpeg", "png", "gif", "mp4", "pdf"}

    # Segurança
    AUTH_TOKEN: str = os.getenv("AUTH_TOKEN", "")

settings = Settings()
