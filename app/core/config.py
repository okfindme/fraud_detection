from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str
    APP_ENV: str = "dev"


# Instantiated once at module level — .env is read once,
# same object reused across the entire app.
settings = Settings() 
# Create Settings() once at module level so the .env file is loaded only once
# and the same shared settings object is reused across the entire app.
# otherwise file is loaded everytime Setting is imported in some file , taking up a memory space
