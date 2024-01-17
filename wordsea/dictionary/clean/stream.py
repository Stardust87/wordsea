import json
from collections import defaultdict
from typing import Any

import pandas as pd
from tqdm import tqdm

from wordsea.dictionary.clean.constraints import (
    filter_nonaplha_examples,
    has_correct_word,
    has_phonetics,
    has_raw_tag_to_skip,
    is_language,
    is_redirect,
    is_vulgar,
    starts_with_number,
)
from wordsea.dictionary.clean.entry import Entry


class WikiRawStream:
    def __init__(self, path: str):
        self.path = path
        self.redirects = []
        self.entries = defaultdict(list)
        self.n_valid = 0

    def filter_senses(self, word: str, senses: list[dict[str, Any]]):
        new_senses = {}

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
                if has_raw_tag_to_skip(sense):
                    continue

            gloss = sense["glosses"][0]

            if not gloss in new_senses:
                if starts_with_number(gloss):
                    continue
                if "examples" in sense:
                    sense["examples"] = filter_nonaplha_examples(sense["examples"])
                else:
                    sense["examples"] = []
                new_senses[gloss] = sense
            else:
                if "examples" in sense:
                    new_senses[gloss]["examples"].extend(
                        filter_nonaplha_examples(sense["examples"])
                    )

        return list(new_senses.values())

    def forms_to_aliases(self, word: str, forms: list[dict[str, Any]]) -> None:
        for form in forms:
            self.redirects.append(
                {
                    "title": form["form"],
                    "redirect": word,
                }
            )

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

                if is_redirect(entry):
                    self.redirects.append(
                        {
                            "title": entry["title"],
                            "redirect": entry["redirect"],
                        }
                    )
                    continue
                if not is_language(entry):
                    continue
                if not has_correct_word(entry):
                    continue
                if not has_phonetics(entry):
                    continue
                if is_vulgar(entry):
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

    def entry_info(self, entry: Entry) -> dict[str, Any]:
        return {
            "id": entry.id,
            "word": entry.word,
        }

    def export(self):
        redirects = pd.DataFrame(self.redirects)
        redirects = redirects.drop_duplicates(subset=["title"])
        for r in redirects.itertuples():
            if r.redirect in self.entries:
                for entry in self.entries[r.redirect]:
                    entry.aliases.add(r.title)

        info_records = []
        out_path = self.path.replace(".json", "-minimal.json")
        with open(out_path, "w", encoding="utf-8") as out_file:
            for entries in tqdm(self.entries.values(), desc="Exporting"):
                for entry in entries:
                    out_file.write(json.dumps(entry.to_dict()) + "\n")
                    info_records.append(self.entry_info(entry))

        info = pd.DataFrame(info_records)
        info.to_csv(out_path.replace(".json", "-info.csv"), index=False)
