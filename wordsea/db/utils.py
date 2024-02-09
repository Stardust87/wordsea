from typing import Any

from mongoengine import connect

from wordsea.constants import MONGODB_URL


class MongoDB:
    def __init__(self, url: str = MONGODB_URL) -> None:
        self.client = connect("wordsea", host=url)

    def __enter__(self) -> "MongoDB":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.client.close()
