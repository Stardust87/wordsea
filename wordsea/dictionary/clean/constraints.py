import re
from typing import Any


def has_raw_tag_to_skip(
    sense: dict[str, Any], skip_raw_tags=["obsolete", "archaic", "slang"]
) -> bool:
    gloss_tag = re.search(r"\((.*?)\)", sense["raw_glosses"][0])
    if gloss_tag:
        gloss_tag = gloss_tag.group(1)
        if "," in gloss_tag:
            gloss_tag = [tag.strip() for tag in gloss_tag.split(",")]
        else:
            gloss_tag = [gloss_tag]

        if any([tag in skip_raw_tags for tag in gloss_tag]):
            return True

    return False


def is_language(entry: dict[str, Any], code: str = "en") -> bool:
    return entry["lang_code"] == code


def has_correct_word(entry: dict[str, Any]) -> bool:
    if not "word" in entry:
        return False

    letters = re.sub(r"[^A-Za-z\s\-\']+", "", entry["word"])
    first_letter = entry["word"][0]
    return all(
        [
            len(letters) >= 3,
            len(letters) == len(entry["word"]),
            first_letter.isalnum(),
            not first_letter.isupper(),
        ]
    )


def is_redirect(entry: dict[str, Any]) -> bool:
    return "redirect" in entry


def has_phonetics(entry: dict[str, Any]) -> bool:
    if not "sounds" in entry:
        return False

    for sound in entry["sounds"]:
        if "ipa" in sound:
            return True

    return False


def is_vulgar(entry: dict[str, Any]) -> bool:
    return "vulgar" in entry.get("tags", []) or "fuck" in entry["word"]
