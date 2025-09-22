from app.infrastructure.common.config import Config
from celery import Celery


config = Config()
worker_app = Celery(
    "worker",
    broker=config.redis.uri,
    backend=config.redis.uri,
    include=["app.infrastructure.celery.tasks"],
)

if __name__ == "__main__":
    worker_app.worker_main(["worker", "--loglevel=info"])
