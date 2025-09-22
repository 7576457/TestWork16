from abc import ABC, abstractmethod

from app.domain.quote.entity import Quote


class QuoteService(ABC):
    @abstractmethod
    async def parse(self) -> list[Quote]:
        pass
