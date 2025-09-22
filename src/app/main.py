import logging

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.infrastructure.common.config import Config
from app.ioc import AppProvider
from app.presentation.web.routes import quote
from dishka import make_async_container

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(name)s: %(message)s",
)


def get_fastapi_app() -> FastAPI:
    config = Config()
    container = make_async_container(AppProvider(), context={Config: config})
    app = FastAPI(title="Quotes Scraper API")
    setup_dishka(container, app)
    app.include_router(quote.router)
    return app


if __name__ == "__main__":
    uvicorn.run(get_fastapi_app())
