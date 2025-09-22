from dataclasses import dataclass


@dataclass(frozen=True)
class Author:
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Author name cannot be empty")


@dataclass(frozen=True)
class Text:
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Quote text cannot be empty")
        if len(self.value) > 1000:
            raise ValueError("Quote text is too long")


@dataclass(frozen=True)
class Tag:
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Tag cannot be empty")
        if " " in self.value:
            raise ValueError("Tag cannot contain spaces")
