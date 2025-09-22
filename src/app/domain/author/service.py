from abc import ABC, abstractmethod

from app.domain.quote.repository import QuoteRepository
from app.domain.quote.entity import Quote


class QuoteParserService(ABC):
    def __init__(self, repository: QuoteRepository):
        self.repository = repository

    @abstractmethod
    async def parse(self) -> list[Quote]:
        pass
