import os

DB_SQLITE_PATH = os.getenv("DB_SQLITE_PATH", "app.db")
DB_POSTGRES_URL = os.getenv("DB_POSTGRES_URL", "postgresql://user:pass@localhost/db")
DB_MONGODB_URL = os.getenv("DB_MONGODB_URL", "mongodb://localhost:27017")
DB_REDIS_URL = os.getenv("DB_REDIS_URL", "redis://localhost:6379")
