import json
import logging
from collections import defaultdict

from wordsea.db import Word

logging.basicConfig(
    format="%(levelname)s - %(message)s",
    level=logging.WARNING,
)


def find_words(
    words: list[str],
) -> dict[str, list[Word]]:
    found_words = defaultdict(list)
    not_found = []

    for word in words:
        if query_words := Word.objects(word=word):
            found_words[str(word)] = [
                json.loads(word.to_json()) for word in query_words
            ]
        else:
            not_found.append(word)

    if not_found:
        logging.warning(f"The following words were not found: {', '.join(not_found)}")

    return found_words
