from loguru import logger
from pydantic_settings import BaseSettings
from dotenv import  load_dotenv

load_dotenv()

class Settings(BaseSettings):
    discord_token: str
    mongo_db_uri: str
    mongo_db_name: str
    owner_id: int

    class Config:
        env_file = ".env"
        case_sensitive = False


try:
    settings = Settings()
except Exception as e:
    logger.error(f"Error loading settings: {e}")
    raise