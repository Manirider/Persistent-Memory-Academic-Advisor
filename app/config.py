from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    DB_PATH: str = "/app/data/advisor_memory.db"
    CHROMA_DB_PATH: str = "/app/data/chroma_db"
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    
    MCP_TRANSPORT: str = "stdio"
    MCP_SERVER_NAME: str = "academic-advisor-mcp"
    
    TOP_K_DEFAULT: int = 5
    MAX_TOP_K: int = 50
    MAX_CONTENT_LENGTH: int = 10000
    
    EMBEDDING_DEVICE: str = "cpu"

    model_config = ConfigDict(env_file=".env", extra="ignore")


settings = Settings()
