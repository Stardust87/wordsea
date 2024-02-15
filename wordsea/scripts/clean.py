from typing import Optional

import click

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
def clean(path: str, words_subset_path: Optional[str]) -> None:
    """Clean the raw Wiktionary data.

    PATH (str): path to raw Wiktionary data (JSON)

    """
    stream = WikiRawStream(path=path, words_subset_path=words_subset_path)
    stream.process()
    stream.export()
