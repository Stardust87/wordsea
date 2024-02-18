from typing import Optional

import click

from wordsea.db import MongoDB
from wordsea.dictionary.clean import WikiRawStream


@click.command(
    epilog="Download pre-extracted data from https://kaikki.org/dictionary/rawdata.html."
)
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--words-subset-path",
    "-w",
    type=click.Path(exists=True),
    help="Path to a file with words to process. If not provided, all words will be processed.",
    default=None,
)
@click.option("-i", "--index", is_flag=True, help="Create a Typesense index.")
def clean(path: str, words_subset_path: Optional[str], index: bool) -> None:
    """Clean the raw Wiktionary data.

    PATH (str): path to raw Wiktionary data (JSON)

    """
    stream = WikiRawStream(path=path, words_subset_path=words_subset_path)
    stream.process()

    with MongoDB():
        stream.export()
        if index:
            stream.index()
