from logging import getLogger

from app.application.interactors import (
    GetQuotesInteractor,
    QuoteFilter,
)
from app.domain.quote.exceptions import QuoteNotFound
from app.infrastructure.celery.tasks import create_quotes_task
from app.infrastructure.common.config import Config
from app.infrastructure.mongo.repositories import MongoQuoteRepository
from dishka.integrations.fastapi import DishkaRoute, FromDishka  # noqa: F401
from fastapi import APIRouter, HTTPException, Query
from pymongo import AsyncMongoClient


logger = getLogger(__name__)
router = APIRouter(tags=["Quotes"], route_class=DishkaRoute)


@router.post("/parse-quotes-task")
async def parse_quotes_task():
    task = create_quotes_task.delay()
    return task.id


@router.get("/quotes")
async def quotes(
    author: str = Query(None, description="Filter by author"),
    tag: str = Query(None, description="Filter by tag"),
):
    try:
        config = Config()
        client = AsyncMongoClient(config.mongodb.uri)
        repo = MongoQuoteRepository(client, config)
        interactor = GetQuotesInteractor(repo)
        filter = QuoteFilter(author=author, tag=tag)

        return await interactor.execute(filter)
    except QuoteNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


# @router.post("/parse-quotes-task", response_model=None)
# async def parse_quotes_task(interactor: FromDishka[CreateQuotesInteractor]):
#     return await interactor.execute()


# @router.get("/quotes")
# async def quotes(
#     interactor: FromDishka[GetQuotesInteractor],
#     author: str = Query(None, description="Filter by author"),
#     tag: str = Query(None, description="Filter by tag"),
# ):
#     try:
#         filter = QuoteFilter(author=author, tag=tag)
#         return await interactor.execute(filter)
#     except QuoteNotFound as e:
#         raise HTTPException(status_code=404, detail=str(e))
