import json
from pathlib import Path
from typing import Any

from tqdm import tqdm

from wordsea.db.schema import Meaning
from wordsea.dictionary.clean.constraints import (
    filter_nonalpha_examples,
    has_correct_word,
    is_language,
    is_vulgar,
    starts_with_number,
)
from wordsea.dictionary.clean.index import create_typesense_index
from wordsea.gen import parse_input_words


class WikiRawStream:
    def __init__(
        self,
        path: str,
        words_subset_path: str,
    ):
        self.path = Path(path)
        self.words_subset = set(parse_input_words([words_subset_path]))

        self.derived: dict[str, str] = self.find_derived()  # derived word -> base word
        self.meanings: list[Meaning] = self.process()

    def filter_senses(self, senses: list[dict[str, Any]]) -> list[dict[str, Any]]:
        new_senses = {}

        for sense in senses:
            if "alt_of" in sense or "form_of" in sense or "glosses" not in sense:
                continue

            if "synonyms" in sense:
                is_synonym_of = False
                for synonym in sense["synonyms"]:
                    if "synonym-of" in synonym.get("tags", []):
                        is_synonym_of = True
                        break

                if is_synonym_of:
                    continue

            gloss = sense["glosses"][0]

            if gloss not in new_senses:
                if starts_with_number(gloss):
                    continue
                if "examples" in sense:
                    sense["examples"] = filter_nonalpha_examples(sense["examples"])
                else:
                    sense["examples"] = []
                new_senses[gloss] = sense
            else:
                if "examples" in sense:
                    new_senses[gloss]["examples"].extend(
                        filter_nonalpha_examples(sense["examples"])
                    )

        return list(new_senses.values())

    def find_derived(self) -> dict[str, str]:
        derived_words: dict[str, str] = {}

        with self.path.open(encoding="utf-8") as raw_file:
            for line in tqdm(raw_file, desc="Finding derived words"):
                entry = json.loads(line)

                if entry.get("word", None) in self.words_subset and is_language(entry):
                    for derived in entry.get("derived", []):
                        if (
                            "word" in derived
                            and derived["word"] not in self.words_subset
                        ):
                            derived_words[derived["word"]] = entry["word"]

        return derived_words

    def process(self) -> list[Meaning]:
        meanings: list[Meaning] = []

        with self.path.open(encoding="utf-8") as raw_file:
            pbar = tqdm(enumerate(raw_file), desc="Cleaning")
            for idx, line in pbar:
                pbar.set_postfix(
                    {
                        "pct_valid": f"{len(meanings) / (idx + 1):.2%}",
                        "n_valid": f"{len(meanings)/1000:.1f}K",
                    }
                )
                entry = json.loads(line)

                if "word" not in entry:
                    continue

                if entry["word"] not in self.words_subset:
                    if entry["word"] in self.derived:
                        entry["derived_from"] = self.derived[entry["word"]]
                    else:
                        continue

                if not is_language(entry):
                    continue
                if not has_correct_word(entry):
                    continue
                if is_vulgar(entry):
                    continue

                entry["senses"] = self.filter_senses(entry["senses"])
                if not entry["senses"]:
                    continue

                meanings.append(Meaning.from_wiktionary(entry))

        return meanings

    def upload(self) -> None:
        Meaning.drop_collection()
        Meaning.objects.insert(self.meanings)
        create_typesense_index()
