from app.domain.quote.repository import QuoteRepository
from app.domain.quote.service import QuoteService


class CreateQuotesInteractor:
    def __init__(self, service: QuoteService, repository: QuoteRepository):
        self._service = service
        self._repository = repository

    async def execute(self) -> None:
        quotes = await self._service.parse()
        await self._repository.save_many(quotes)
