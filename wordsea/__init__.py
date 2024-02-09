import click

from wordsea.scripts import clean, find, generate, imagine


@click.group()
def main():
    """WordSea command line interface."""


main.add_command(clean)
main.add_command(find)
main.add_command(generate)
main.add_command(imagine)
