from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Placement RAG Assistant"
    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3000
    DATABASE_URL: str = ""
    GOOGLE_API_KEY: str = ""
    EMBEDDING_MODEL: str = "models/embedding-001"
    CHAT_MODEL: str = "gemini-pro"
    UPLOAD_DIR: str = "./uploads"
    VECTOR_DB_DIR: str = "./vector_db"

    class Config:
        env_file = ".env"

settings = Settings()