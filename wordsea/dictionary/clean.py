import json
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Optional


import pandas as pd
from tqdm import tqdm


@dataclass
class Example:
    text: str
    ref: Optional[str] = None
    type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        return cls(
            text=data["text"],
            ref=data.get("ref", None),
            type=data.get("type", None),
        )


@dataclass
class Sense:
    gloss: str
    raw_gloss: Optional[str]
    examples: list[Example]


@dataclass
class Entry:
    id: int
    word: str
    pos: str
    senses: list[Sense]
    aliases: Optional[set[str]] = None

    def __post_init__(self):
        if self.aliases is None:
            self.aliases = set()

    @classmethod
    def from_dict(cls, id: int, data: dict[str, Any]):
        return cls(
            id=id,
            word=data["word"],
            pos=data["pos"],
            senses=[
                Sense(
                    gloss=sense["glosses"][0],
                    raw_gloss=sense["raw_glosses"][0]
                    if "raw_glosses" in sense
                    else None,
                    examples=[
                        Example.from_dict(ex) for ex in sense.get("examples", [])
                    ],
                )
                for sense in data["senses"]
            ],
        )

    def to_dict(self):
        return {
            "id": self.id,
            "word": self.word,
            "pos": self.pos,
            "senses": [
                {
                    "gloss": sense.gloss,
                    "raw_gloss": sense.raw_gloss,
                    "examples": [ex.__dict__ for ex in sense.examples],
                }
                for sense in self.senses
            ],
            "aliases": list(self.aliases),
        }


class WikiRawStream:
    def __init__(self, path: str = "/mnt/Sidra/wiktionary/raw-wiktextract-data.json"):
        self.path = path
        self.redirects = []
        self.entries = defaultdict(list)
        self.n_valid = 0

    def filter_senses(self, word: str, senses: list[dict[str, Any]]):
        new_senses = []

        for sense in senses:
            if "form_of" in sense:
                for form in sense["form_of"]:
                    if "word" in form:
                        self.redirects.append(
                            {
                                "title": word,
                                "redirect": form["word"],
                            }
                        )
                continue

            elif "alt_of" in sense:
                for alt in sense["alt_of"]:
                    if "word" in alt:
                        self.redirects.append(
                            {
                                "title": word,
                                "redirect": alt["word"],
                            }
                        )
                continue

            elif "glosses" not in sense:
                continue

            elif "raw_glosses" in sense:
                if self.has_raw_tag_to_skip(sense):
                    continue

            new_senses.append(sense)

        return new_senses

    def forms_to_aliases(self, word: str, forms: list[dict[str, Any]]) -> None:
        for form in forms:
            self.redirects.append(
                {
                    "title": form["form"],
                    "redirect": word,
                }
            )

    @staticmethod
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

    @staticmethod
    def is_language(entry: dict[str, Any], code: str = "en") -> bool:
        return entry["lang_code"] == code

    @staticmethod
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

    @staticmethod
    def is_redirect(entry: dict[str, Any]) -> bool:
        return "redirect" in entry

    @staticmethod
    def has_phonetics(entry: dict[str, Any]) -> bool:
        if not "sounds" in entry:
            return False

        for sound in entry["sounds"]:
            if "ipa" in sound:
                return True

        return False

    @staticmethod
    def is_vulgar(entry: dict[str, Any]) -> bool:
        return "vulgar" in entry.get("tags", []) or "fuck" in entry["word"]

    def process(self):
        out_path = self.path.replace(".json", "-filtered.json")
        out_file = open(out_path, "w", encoding="utf-8")

        with open(self.path, encoding="utf-8") as raw_file:
            for idx, line in (
                pbar := tqdm(enumerate(raw_file), desc="Cleaning")
            ):  # raw 9401685
                pbar.set_postfix(
                    {
                        "pct_valid": f"{self.n_valid / (idx + 1):.2%}",
                        "pct_redirects": f"{len(self.redirects) / (idx + 1):.2%}",
                        "n_valid": f"{self.n_valid/1000:.1f}K",
                        "n_redirects": f"{len(self.redirects)/1000:.1f}K",
                    }
                )

                entry = json.loads(line)

                if self.is_redirect(entry):
                    self.redirects.append(
                        {
                            "title": entry["title"],
                            "redirect": entry["redirect"],
                        }
                    )
                    continue
                if not self.is_language(entry):
                    continue
                if not self.has_correct_word(entry):
                    continue
                if not self.has_phonetics(entry):
                    continue
                if self.is_vulgar(entry):
                    continue

                if "forms" in entry:
                    self.forms_to_aliases(entry["word"], entry["forms"])

                entry["senses"] = self.filter_senses(entry["word"], entry["senses"])
                if not entry["senses"]:
                    continue

                entry = Entry.from_dict(self.n_valid, entry)
                self.entries[entry.word].append(entry)
                self.n_valid += 1
                out_file.write(line)

        out_file.close()

    def export(self):
        redirects = pd.DataFrame(self.redirects)
        redirects = redirects.drop_duplicates(subset=["title"])
        for r in redirects.itertuples():
            if r.redirect in self.entries:
                for entry in self.entries[r.redirect]:
                    entry.aliases.add(r.title)

        out_path = self.path.replace(".json", "-minimal.json")
        with open(out_path, "w", encoding="utf-8") as out_file:
            for entries in tqdm(self.entries.values(), desc="Exporting"):
                for entry in entries:
                    out_file.write(json.dumps(entry.to_dict()) + "\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Clean the raw Wiktionary data.",
        epilog="Download pre-extracted data from https://kaikki.org/dictionary/rawdata.html.",
    )
    parser.add_argument("path", type=str, help="path to raw Wiktionary data (JSON)")
    args = parser.parse_args()

    stream = WikiRawStream(path=args.path)
    stream.process()
    stream.export()
