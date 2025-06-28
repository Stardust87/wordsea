import click

from wordsea.scripts import clean, find, generate, imagine


@click.group()
def main() -> None:
    """WordSea command line interface."""


main.add_command(clean)  # type: ignore[arg-type]
main.add_command(find)  # type: ignore[arg-type]
main.add_command(generate)  # type: ignore[arg-type]
main.add_command(imagine)  # type: ignore[arg-type]
