import click
from tqdm import tqdm

from wordsea.constants import LLAMACPP_URL
from wordsea.db import Meaning, Mnemonic, MongoDB
from wordsea.dictionary import find_words
from wordsea.gen import LlamaCppAPI, parse_input_words, render_definition, render_prompt


def generate_image_prompts(model: str, entries: dict[str, list[Meaning]]) -> None:
    api = LlamaCppAPI(url=LLAMACPP_URL, model=model)
    if not api.health():
        raise RuntimeError("API is not healthy")

    pbar = tqdm(entries.items(), total=len(entries), desc="Generating image prompts")
    for word, entry in pbar:
        pbar.set_postfix_str(word)
        html = render_definition(entry)
        prompt = render_prompt(word, html)

        answer = api.generate(word, prompt)
        if answer is None:
            continue

        mnemonic = Mnemonic(
            word=word,
            explanation=answer["explanation"],
            prompt=answer["prompt"],
            language_model=model,
        )
        mnemonic.save()


@click.command()
@click.argument("words", nargs=-1, type=str, required=True)
@click.option(
    "-m", "--model", type=str, default="mixtral", help="language model to use"
)
@click.option(
    "-n",
    "--new",
    is_flag=True,
    help="whether to generate prompts only for words that are not in the database",
)
def generate(words, model, new) -> None:
    """Generate image prompts for words.

    WORDS (list[str]): words to generate prompts for - every entity can be either a word or a path to a file with words separated by newlines
    """

    words = parse_input_words(words)

    with MongoDB():
        if new:
            generated = [mnemo.word for mnemo in Mnemonic.objects(word__in=words)]
            words = [word for word in words if word not in generated]

        if not words:
            click.echo("all prompts are already generated")
            exit(0)

        entries = find_words(words)
        generate_image_prompts(model, entries)
