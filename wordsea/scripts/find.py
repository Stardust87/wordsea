import json

import click

from wordsea.db import MongoDB
from wordsea.dictionary import find_words
from wordsea.gen import parse_input_words


@click.command()
@click.argument("words", nargs=-1, type=str, required=True)
def find(words) -> None:
    """Find words in JSON dictionary cleaned using `wordsea clean`.

    WORDS (list[str]): words to find - every entity can be either a word or a path to a file with words separated by newlines
    """

    words = parse_input_words(words)

    with MongoDB():
        entries = find_words(words)

    click.echo(json.dumps(entries, indent=2))
