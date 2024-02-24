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
    required=True,
    help="Path to a file with words to process. If not provided, all words will be processed.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Do not write to the database or Typesense.",
)
def clean(path: str, words_subset_path: str, dry_run: bool) -> None:
    """Clean the raw Wiktionary data.

    PATH (str): path to raw Wiktionary data (JSON)

    """
    stream = WikiRawStream(path, words_subset_path)

    if not dry_run:
        with MongoDB():
            stream.upload()
