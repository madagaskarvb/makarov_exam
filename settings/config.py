from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    DATABASE_URL : str
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int
    REDIS_URL : int

    model_config = SettingsConfigDict(
    env_file = ".env",
    env_file_encoding="utf-8",
    case_sensitive=True,
    extra="ignore"
)
    
settings = Settings()