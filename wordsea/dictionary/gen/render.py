import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

import wordsea

TEMPLATES_PATH = Path(wordsea.__file__).parent / "dictionary" / "templates"


def render_definition(entries) -> str:
    env = Environment(loader=FileSystemLoader(TEMPLATES_PATH))
    template = env.get_template("definition.html")
    return template.render(entries=entries)


def render_prompt(word: str, definition: str) -> str:
    definition = re.sub(r"\s\s+", " ", definition)
    definition = definition.replace("\n", "")

    env = Environment(loader=FileSystemLoader(TEMPLATES_PATH))
    template = env.get_template("prompt.html")
    return template.render(word=word, definition=definition)