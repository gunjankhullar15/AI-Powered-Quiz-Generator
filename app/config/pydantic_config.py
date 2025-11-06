from pydantic_settings import BaseSettings
from pydantic import ConfigDict, computed_field

class Settings(BaseSettings):
    db_host: str
    db_port: str
    db_name: str
    db_user: str
    db_password: str
    openai_api_key: str
    base_url: str  
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra='ignore'
    )
    
    @computed_field
    @property
    def database_url(self) -> str:
        """Construct database URL from individual components"""
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

settings = Settings()