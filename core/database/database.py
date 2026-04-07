from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings


class Database:
    _client: AsyncIOMotorClient = None
    _db = None


    @classmethod
    async def connect(cls):
        """Establish connection to database."""
        try:
            cls._client = AsyncIOMotorClient(settings.mongo_db_uri)
            cls._db = cls._client[settings.mongo_db_name]
            # verify connection
            await cls._client.admin.command("ping")
            logger.info(f"Connected to MongoDB database")
        except Exception as e:
            logger.error(f"Error connecting to MongoDB database: {e}")
            raise e

    @classmethod
    async def close(cls):
        """Close connection to database."""
        if cls._client is not None:
            cls._client.close()
            logger.warning(f"Closed connection to MongoDB database")

    @classmethod
    async def get_db(cls):
        if cls._db is None:
            await cls.connect()
        return cls._db

    @classmethod
    async def sticky_message_collection(cls):
        return cls._db.sticky_messages