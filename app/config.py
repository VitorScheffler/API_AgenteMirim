import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = (
    f"postgresql+asyncpg://"
    f"{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', 'postgres')}"
    f"@{os.getenv('DB_HOST', 'db')}:{os.getenv('DB_PORT', '5432')}"
    f"/{os.getenv('DB_NAME', 'agentemirim_db')}"
)

UPLOAD_DIR     = os.getenv("UPLOAD_DIR", "/data/uploads")
AUTH_TOKEN     = os.getenv("AUTH_TOKEN", "")
MAX_UPLOAD_MB  = int(os.getenv("MAX_UPLOAD_MB", "0"))
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "mp4", "pdf", "webp"}

def validar():
    if not AUTH_TOKEN:
        raise RuntimeError("AUTH_TOKEN não definido no .env")
    if len(AUTH_TOKEN) < 16:
        raise RuntimeError("AUTH_TOKEN muito curto — mínimo 16 caracteres")
