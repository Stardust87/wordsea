from typing import Any

import regex as re


def starts_with_number(gloss: str) -> bool:
    pattern = r"^[0-9][^-]"
    return bool(re.match(pattern, gloss))


def filter_nonalpha_examples(examples: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pattern = r"^\W+$"
    new_examples: list[dict[str, Any]] = []
    for example in examples:
        if not re.match(pattern, example["text"]):
            new_examples.append(example)
    return new_examples


def is_language(entry: dict[str, Any], code: str = "en") -> bool:
    return entry["lang_code"] == code


def has_correct_word(entry: dict[str, Any]) -> bool:
    if "word" not in entry:
        return False

    word = entry["word"]
    letters = re.sub(r"[^\p{Ll}]+", "", word)
    first_letter = word[0]
    last_letter = word[-1]
    return all(
        [
            len(letters) >= 3,
            len(letters) == len(word),
            not first_letter.isupper(),
            last_letter.isalpha(),
        ]
    )


def is_vulgar(entry: dict[str, Any]) -> bool:
    return "vulgar" in entry.get("tags", []) or "fuck" in entry["word"]
