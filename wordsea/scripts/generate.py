import json

import click
from tqdm import tqdm

from wordsea.constants import LLAMACPP_URL, LOGS_PATH, PromptModel
from wordsea.db import Meaning, Mnemonic, MongoDB
from wordsea.dictionary import find_words
from wordsea.gen import (
    LlamaCppAPI,
    parse_input_words,
    render_definition,
    render_prompt,
    render_prompt_derived,
)


def generate_image_prompts(
    model: PromptModel, words: list[str], silent: bool, save_to_file: bool
) -> None:
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

        if not save_to_file:
            mnemonic = Mnemonic(
                word=word,
                explanation=answer["explanation"],
                prompt=answer["prompt"],
                language_model=model,
            )
            mnemonic.save()
        else:
            output_path = LOGS_PATH / "prompts" / model / f"{word}.json"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with output_path.open("w") as f:
                json.dump(answer, f, indent=2)


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
    "-d",
    "--derived",
    is_flag=True,
    help="whether to generate prompts only for derived words",
)
@click.option(
    "-s",
    "--silent",
    is_flag=True,
    help="whether to suppress the finding progress bar",
)
@click.option(
    "--save-to-file",
    is_flag=True,
    help="whether to save the generated prompts to a file instead of the database",
)
def generate(
    words: list[str],
    model: PromptModel,
    new: bool,
    limit: int,
    derived: bool,
    silent: bool,
    save_to_file: bool,
) -> None:
    """Generate image prompts for words.

    WORDS (list[str]): words to generate prompts for - every entity can be either a word or a path to a file with words separated by newlines
    """

    with MongoDB():
        if not words:
            words = Meaning.objects(derived_from__exists=derived).distinct("word")
        else:
            words = parse_input_words(words)

        if new:
            generated = [mnemo.word for mnemo in Mnemonic.objects(word__in=words)]
            words = [word for word in words if word not in generated]

        if limit is not None:
            pipeline = [
                {"$group": {"_id": "$word", "count": {"$sum": 1}}},
                {"$match": {"count": {"$lt": limit}}},
                {"$project": {"_id": 0, "word": "$_id", "count": 1}},
            ]
            mnemonic_counts = {
                obj["word"]: obj["count"]
                for obj in Mnemonic.objects().aggregate(pipeline)
            }
            words = [word for word in words if word in mnemonic_counts]

        if not words:
            click.echo("all prompts are already generated")
            exit(0)

        generate_image_prompts(model, words, silent, save_to_file)
