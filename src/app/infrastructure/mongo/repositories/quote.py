import logging
from dataclasses import asdict
from uuid import UUID

from app.domain.quote.entity import Quote
from app.domain.quote.exceptions import (
    AuthorAndTagNotFound,
    AuthorNotFound,
    QuoteNotFound,
    TagNotFound,
)
from app.domain.quote.repository import QuoteRepository
from app.infrastructure.common.config import Config
from pymongo import AsyncMongoClient

logger = logging.getLogger(__name__)


class MongoQuoteRepository(QuoteRepository):
    def __init__(self, client: AsyncMongoClient, config: Config):
        self._client = client
        self._config = config
        self._db = self._client[self._config.mongodb.database]
        self._collection = self._db["quotes"]

    async def save(self, quote: Quote) -> None:
        quote_dict = asdict(quote)
        quote_dict["uuid"] = str(quote_dict["uuid"])
        await self._collection.insert_one(quote_dict)
        logger.info(f"Saved quote {quote.uuid} by {quote.author}")

    async def save_many(self, quotes: list[Quote]) -> None:
        documents = []
        for quote in quotes:
            quote_dict = asdict(quote)
            quote_dict["uuid"] = str(quote_dict["uuid"])
            documents.append(quote_dict)

        await self._collection.insert_many(documents)
        logger.info(f"Saved {len(documents)} quotes")

    async def all(self) -> list[Quote]:
        cursor = self._collection.find({})
        quotes = [
            Quote(
                uuid=UUID(doc["uuid"]),
                author=doc["author"],
                text=doc["text"],
                tags=doc.get("tags", []),
                created_at=doc.get("created_at"),
            )
            async for doc in cursor
        ]
        if not quotes:
            raise QuoteNotFound()
        return quotes


    async def get_by_tag(self, tag: str) -> list[Quote]:
        cursor = self._collection.find({"tags": tag})
        quotes = [
            Quote(
                uuid=UUID(doc["uuid"]),
                author=doc["author"],
                text=doc["text"],
                tags=doc.get("tags", []),
                created_at=doc.get("created_at"),
            )
            async for doc in cursor
        ]
        if not quotes:
            raise TagNotFound(tag)
        return quotes

    async def get_by_author(self, author: str) -> list[Quote]:
        cursor = self._collection.find({"author": author})
        quotes = [
            Quote(
                uuid=UUID(doc["uuid"]),
                author=doc["author"],
                text=doc["text"],
                tags=doc.get("tags", []),
                created_at=doc.get("created_at"),
            )
            async for doc in cursor
        ]
        if not quotes:
            raise AuthorNotFound(author)
        return quotes

    async def get_by_author_and_tag(self, author: str, tag: str) -> list[Quote]:
        cursor = self._collection.find({"author": author, "tags": tag})
        quotes = [
            Quote(
                uuid=UUID(doc["uuid"]),
                author=doc["author"],
                text=doc["text"],
                tags=doc.get("tags", []),
                created_at=doc.get("created_at"),
            )
            async for doc in cursor
        ]
        if not quotes:
            raise AuthorAndTagNotFound(author, tag)
        return quotes
