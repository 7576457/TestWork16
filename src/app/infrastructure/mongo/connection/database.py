import logging

from app.infrastructure.common.config import Config
from pymongo import AsyncMongoClient
from pymongo.errors import ConnectionFailure


logger = logging.getLogger(__name__)


class MongoDatabase:
    def __init__(self, config: Config):
        self._config = config
        self._client: AsyncMongoClient | None = None

    async def connect(self) -> None:
        try:
            uri = self._config.mongodb.uri
            self._client = AsyncMongoClient(uri)
            await self._client.admin.command("ping")
            logger.info(
                f"Connected to MongoDB: {self._config.mongodb.host}:{self._config.mongodb.port}"
            )
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    async def disconnect(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None

    def get_client(self):
        if self._client is None:
            raise RuntimeError("Database not connected")
        return self._client[self._config.mongodb.database]
