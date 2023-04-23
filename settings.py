import os


DEBUG = bool(os.getenv("DEBUG"))

# Database settings.
DB_PROTOCOL = os.getenv("DB_PROTOCOL", "postgresql+asyncpg://")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "phoenix-db")
DB_PARAMS = os.getenv("DB_PARAMS", "")

DATABASE_URL = (
    DB_PROTOCOL
    + ":".join([DB_USER, DB_PASSWORD])
    + "@"
    + (":" if DB_HOST and DB_PORT else "").join([DB_HOST, DB_PORT])
    + "/"
    + DB_NAME
    + DB_PARAMS
)

# CORS settings.
ALLOW_CREDENTIALS = os.getenv("ALLOW_CREDENTIALS", "*").split(",")
ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", "*").split(",")
ALLOW_METHODS = os.getenv("ALLOW_METHODS", "*").split(",")
ALLOW_HEADERS = os.getenv("ALLOW_HEADERS", "*").split(",")

# Uvicorn settings.
PORT = int(os.getenv("PORT", "8080"))
WORKERS = int(os.getenv("WORKERS", "2"))
RELOAD = bool(os.getenv("RELOAD", "1"))
