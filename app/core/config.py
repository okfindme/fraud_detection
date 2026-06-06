from pydantic_settings import BaseSettings , SettingsConfigDict
import os
env = os.getenv("APP_ENV", "dev")
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=f".env.{env}")

    DATABASE_URL: str
    APP_ENV: str = "dev"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    RATE_LIMIT: str = "10/minute"
    ALLOWED_ORIGINS: list[str] = ["*"]


# Instantiated once at module level — .env is read once,
# same object reused across the entire app.
settings = Settings() 
# Create Settings() once at module level so the .env file is loaded only once
# and the same shared settings object is reused across the entire app.
# otherwise file is loaded everytime Setting is imported in some file , taking up a memory space
