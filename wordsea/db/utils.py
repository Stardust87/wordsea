from typing import Any

from mongoengine import connect

from wordsea.config import settings


class MongoDB:
    def __init__(self, url: str | None = None) -> None:
        database_url = url if url is not None else settings.mongodb_url
        self.client = connect("wordsea", host=database_url)

    def __enter__(self) -> "MongoDB":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.client.close()
