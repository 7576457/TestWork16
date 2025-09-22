from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, frozen=True, kw_only=True)
class Author:
    uuid: UUID
    born: str
    name: str
    description: str
