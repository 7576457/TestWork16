from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.quote.entity import Quote


class QuoteRepository(ABC):
    @abstractmethod
    async def save(self, quote: Quote) -> None: ...

    @abstractmethod
    async def all(self) -> list[Quote]: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Quote | None: ...

    @abstractmethod
    async def get_by_tag(self, tag: str) -> list[Quote]: ...

    @abstractmethod
    async def get_by_author(self, author: str) -> list[Quote]: ...
