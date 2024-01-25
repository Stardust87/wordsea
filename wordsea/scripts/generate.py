import argparse
import logging

from tqdm import tqdm

from wordsea import LLAMACPP_URL
from wordsea.db import Mnemonic, MongoDB, Word
from wordsea.dictionary import find_words
from wordsea.gen import LlamaCppAPI, parse_input_words, render_definition, render_prompt


def generate_image_prompts(model: str, entries: dict[str, list[Word]]) -> None:
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "words",
        nargs="+",
        type=str,
        help="words to find - every entity can be either a word or a path to a file with words separated by newlines",
    )
    parser.add_argument("-m", "--model", type=str, default="mixtral")
    parser.add_argument(
        "-n",
        "--new",
        action="store_true",
        help="whether to generate prompts only for words that are not in the database",
    )
    args = parser.parse_args()

    words = parse_input_words(args.words)

    with MongoDB():
        if args.new:
            generated = [mnemo.word for mnemo in Mnemonic.objects(word__in=words)]
            words = [word for word in words if word not in generated]

        if not words:
            logging.info("all prompts are already generated")
            exit(0)

        entries = find_words(words)
        generate_image_prompts(args.model, entries)
