from abc import ABC, abstractmethod

from app.domain.quote.entity import Quote


class QuoteRepository(ABC):
    @abstractmethod
    async def save(self, quote: Quote) -> None: ...

    @abstractmethod
    async def save_many(self, quotes: list[Quote]) -> None: ...

    @abstractmethod
    async def all(self) -> list[Quote]: ...

    @abstractmethod
    async def get_by_tag(self, tag: str) -> list[Quote]: ...

    @abstractmethod
    async def get_by_author(self, author: str) -> list[Quote]: ...

    @abstractmethod
    async def get_by_author_and_tag(self, author: str, tag: str) -> list[Quote]: ...
