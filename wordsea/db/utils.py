from typing import Any, Callable

from mongoengine import connect

from wordsea import MONGODB_URL


def with_mongo(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        client = connect("wordsea", host=MONGODB_URL)
        answer = func(*args, **kwargs)
        client.close()
        return answer

    return wrapper
