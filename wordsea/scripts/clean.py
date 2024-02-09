import click

from wordsea.dictionary.clean import WikiRawStream


@click.command(
    epilog="Download pre-extracted data from https://kaikki.org/dictionary/rawdata.html."
)
@click.argument("path", type=click.Path(exists=True))
def clean(path: str) -> None:
    """Clean the raw Wiktionary data.

    PATH (str): path to raw Wiktionary data (JSON)

    """
    stream = WikiRawStream(path=path)
    stream.process()
    stream.export()
