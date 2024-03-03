import json

import click
from tqdm import tqdm

from wordsea.constants import LLAMACPP_URL
from wordsea.db import Meaning, Mnemonic, MongoDB
from wordsea.dictionary import find_words
from wordsea.gen import (
    LlamaCppAPI,
    parse_input_words,
    render_definition,
    render_prompt,
    render_prompt_derived,
)


def generate_image_prompts(model: str, words: list[str], silent: bool) -> None:
    api = LlamaCppAPI(url=LLAMACPP_URL, model=model)
    if not api.health():
        raise RuntimeError("API is not healthy")

    pbar = tqdm(words, total=len(words), desc="Generating image prompts")
    for word in pbar:
        entry: list[Meaning] = find_words([word], silent=silent)[word]
        pbar.set_postfix_str(word)

        html = render_definition(entry)

        derived_from = {meaning.get("derived_from", None) for meaning in entry}
        derived_from.discard(None)
        derived_word = derived_from.pop() if len(derived_from) == 1 else None

        if derived_word:
            derived_entry = Meaning.objects(word=derived_word)
            derived_entry = [json.loads(entry.to_json()) for entry in derived_entry]
            for meaning in derived_entry:
                for sense in meaning["senses"]:
                    sense["examples"] = []

            derived_html = render_definition(derived_entry)
            prompt = render_prompt_derived(word, html, derived_word, derived_html)
        else:
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
@click.argument("words", nargs=-1, type=str, required=False)
@click.option(
    "-m", "--model", type=str, default="mixtral", help="language model to use"
)
@click.option(
    "-n",
    "--new",
    is_flag=True,
    help="whether to generate prompts only for words that are not in the database",
)
@click.option(
    "-l",
    "--limit",
    type=int,
    default=5,
    help="generate prompts for words with less than this number of images",
)
@click.option(
    "-s",
    "--silent",
    is_flag=True,
    help="whether to suppress the finding progress bar",
)
def generate(words: list[str], model: str, new: bool, limit: int, silent: bool) -> None:
    """Generate image prompts for words.

    WORDS (list[str]): words to generate prompts for - every entity can be either a word or a path to a file with words separated by newlines
    """

    with MongoDB():
        if not words:
            words = Meaning.objects(derived_from__exists=False).distinct("word")
        else:
            words = parse_input_words(words)

        if new:
            generated = [mnemo.word for mnemo in Mnemonic.objects(word__in=words)]
            words = [word for word in words if word not in generated]

        if limit is not None:
            words = [
                word for word in words if Mnemonic.objects(word=word).count() < limit
            ]

        if not words:
            click.echo("all prompts are already generated")
            exit(0)

        generate_image_prompts(model, words, silent)
