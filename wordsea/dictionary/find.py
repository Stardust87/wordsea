import json
import logging
from collections import defaultdict

from tqdm import tqdm

from wordsea.db import Meaning

logging.basicConfig(
    format="%(levelname)s - %(message)s",
    level=logging.WARNING,
)


def find_words(
    words: list[str],
) -> dict[str, list[Meaning]]:
    found_words = defaultdict(list)
    not_found: list[str] = []

    found = 0
    pbar = tqdm(enumerate(words), desc="Finding", total=len(words))
    for _, word in pbar:
        if query_words := Meaning.objects(word=word):
            found_words[str(word)] = [
                json.loads(word.to_json()) for word in query_words
            ]
            found += 1
        else:
            not_found.append(word)

        pbar.set_postfix(
            {
                "found": f"{found}",
                "not_found": f"{len(not_found)}",
            }
        )

    if not_found:
        logging.warning(f"The following words were not found: {', '.join(not_found)}")

    print(f"Found {found} words from {len(words)}")
    return found_words
