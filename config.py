from dotenv import load_dotenv
import os
from sqlalchemy import make_url

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

# === Исправление DATABASE_URL ===
raw_url = os.getenv("DATABASE_URL")

if raw_url:
    # Автоматически исправляем старые варианты
    if raw_url.startswith("postgres://"):
        raw_url = raw_url.replace("postgres://", "postgresql://", 1)

    url = make_url(raw_url)

    # Если нет драйвера asyncpg — добавляем
    if url.drivername in ("postgresql", "postgres"):
        url = url.set(drivername="postgresql+asyncpg")

    DATABASE_URL = str(url)
else:
    raise ValueError("DATABASE_URL не указан в .env файле!")