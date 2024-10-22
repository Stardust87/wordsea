import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

import wordsea
from wordsea.db import Meaning

TEMPLATES_PATH = Path(wordsea.__file__).parent / "dictionary" / "templates"


def parse_input_words(input_words: list[str]) -> list[str]:
    complete_words_list = []
    for word in input_words:
        if Path(word).exists():
            with Path(word).open() as f:
                words = [_word for _word in f.read().splitlines() if word]
                complete_words_list.extend(words)
        else:
            complete_words_list.append(word)

    return sorted(set(complete_words_list))


def render_definition(entries: list[Meaning]) -> str:
    env = Environment(loader=FileSystemLoader(TEMPLATES_PATH))
    template = env.get_template("definition.html")
    return template.render(entries=entries)


def render_prompt(word: str, definition: str) -> str:
    definition = re.sub(r"\s\s+", " ", definition)
    definition = definition.replace("\n", "")

    env = Environment(loader=FileSystemLoader(TEMPLATES_PATH))
    template = env.get_template("prompt.html")
    return template.render(word=word, definition=definition)


def render_prompt_derived(
    word: str, definition: str, derived_word: str, derived_definition: str
) -> str:
    definition = re.sub(r"\s\s+", " ", definition)
    definition = definition.replace("\n", "")

    derived_definition = re.sub(r"\s\s+", " ", derived_definition)
    derived_definition = derived_definition.replace("\n", "")

    env = Environment(loader=FileSystemLoader(TEMPLATES_PATH))
    template = env.get_template("prompt-derived.html")
    return template.render(
        word=word,
        definition=definition,
        derived_word=derived_word,
        derived_definition=derived_definition,
    )
