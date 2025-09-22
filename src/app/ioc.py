from pymongo import AsyncMongoClient

from app.application.interactors import CreateQuotesInteractor, GetQuotesInteractor
from app.domain.quote.repository import QuoteRepository
from app.domain.quote.service import QuoteService
from app.infrastructure.common.config import Config
from app.infrastructure.mongo.connection import MongoDatabase
from app.infrastructure.mongo.repositories import MongoQuoteRepository
from app.infrastructure.scrapy.quote import ParseQuotesService
from dishka import Provider, Scope, from_context, provide


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_mongo_database(self, config: Config) -> MongoDatabase:
        mongodb = MongoDatabase(config)
        await mongodb.connect()
        return mongodb

    @provide(scope=Scope.REQUEST)
    def get_mongo_client(self, mongodb: MongoDatabase) -> AsyncMongoClient:
        return mongodb.get_client()

    mongo_quote_repository = provide(
        MongoQuoteRepository, provides=QuoteRepository, scope=Scope.REQUEST
    )
    parse_quotes_service = provide(
        ParseQuotesService, provides=QuoteService, scope=Scope.REQUEST
    )

    create_quotes_interactor = provide(CreateQuotesInteractor, scope=Scope.REQUEST)

    get_quotes_interactor = provide(GetQuotesInteractor, scope=Scope.REQUEST)
