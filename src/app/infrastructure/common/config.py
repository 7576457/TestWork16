from dataclasses import dataclass, field
from os import environ as env

from dotenv import load_dotenv

load_dotenv()


@dataclass(slots=True)
class RedisConfig:
    host: str = field(default_factory=lambda: env.get("REDIS_HOST"))
    port: str = field(default_factory=lambda: env.get("REDIS_PORT"))
    user: str | None = field(default_factory=lambda: env.get("REDIS_USER"))
    password: str | None = field(default_factory=lambda: env.get("REDIS_PASS"))
    database: str = field(default_factory=lambda: env.get("REDIS_DB"))

    @property
    def uri(self) -> str:
        return f"redis://{self.host}:{self.port}/0"


@dataclass(slots=True)
class MongoConfig:
    host: str = field(default_factory=lambda: env.get("MONGO_HOST"))
    port: str = field(default_factory=lambda: env.get("MONGO_PORT"))
    user: str | None = field(default_factory=lambda: env.get("MONGO_USER"))
    password: str | None = field(default_factory=lambda: env.get("MONGO_PASS"))
    database: str = field(default_factory=lambda: env.get("MONGO_DB"))

    @property
    def uri(self) -> str:
        if self.user and self.password:
            return f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}/"
        return f"mongodb://{self.host}:{self.port}/"


@dataclass(slots=True)
class Config:
    mongodb: MongoConfig = field(default_factory=MongoConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)
