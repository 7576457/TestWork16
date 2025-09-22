from dataclasses import dataclass

from app.domain.quote.entity import Quote
from app.domain.quote.repository import QuoteRepository


@dataclass
class QuoteFilter:
    author: str | None = None
    tag: str | None = None


class GetQuotesInteractor:
    def __init__(self, repository: QuoteRepository):
        self._repository = repository

    async def execute(self, filter: QuoteFilter | None = None) -> list[Quote]:
        if filter:
            if filter.author is not None and filter.tag is not None:
                return await self._repository.get_by_author_and_tag(filter.author, filter.tag)
            elif filter.tag is not None:
                return await self._repository.get_by_tag(filter.tag)
            elif filter.author is not None:
                return await self._repository.get_by_author(filter.author)

        return await self._repository.all()
