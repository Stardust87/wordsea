import argparse
import json
import logging

from wordsea.db import MongoDB
from wordsea.dictionary import find_words
from wordsea.gen import parse_input_words


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Find words in JSON dictionary cleaned using `wordsea clean`.",
    )
    parser.add_argument(
        "words",
        nargs="+",
        type=str,
        help="words to find - every entity can be either a word or a path to a file with words separated by newlines",
    )
    args = parser.parse_args()

    words = parse_input_words(args.words)

    with MongoDB():
        entries = find_words(words)

    logging.info(json.dumps(entries, indent=2))
