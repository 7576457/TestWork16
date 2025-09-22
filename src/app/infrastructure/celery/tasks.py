import asyncio
import logging

from app.application.interactors.create_quotes import CreateQuotesInteractor
from app.infrastructure.celery.worker import worker_app
from app.infrastructure.common.config import Config
from app.infrastructure.mongo.repositories import MongoQuoteRepository
from app.infrastructure.scrapy.quote import ParseQuotesService
from pymongo import AsyncMongoClient

logger = logging.getLogger(__name__)


@worker_app.task()
def create_quotes_task():
    config = Config()
    client = AsyncMongoClient(config.mongodb.uri)
    repo = MongoQuoteRepository(client, config)
    parser = ParseQuotesService()
    interactor = CreateQuotesInteractor(parser, repo)

    asyncio.run(interactor.execute())
