import json
from pathlib import Path
from typing import Any

import pandas as pd
from mongoengine import connect
from tqdm import tqdm

from wordsea import MONGODB_URL
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
from wordsea.dictionary.schema import Redirect, Word


class WikiRawStream:
    def __init__(self, path: str):
        self.path = Path(path)
        self.redirects: list[Redirect] = []
        self.words: list[Word] = []

    def filter_senses(
        self, word: str, senses: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        new_senses = {}

        for sense in senses:
            if "form_of" in sense:
                for form in sense["form_of"]:
                    if "word" in form:
                        self.redirects.append(
                            Redirect(from_word=word, to_word=form["word"])
                        )
                continue

            elif "glosses" not in sense:
                continue

            elif "raw_glosses" in sense:
                if has_raw_tag_to_skip(sense):
                    continue

            gloss = sense["glosses"][0]

            if gloss not in new_senses:
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

    def process(self) -> None:
        with self.path.open(encoding="utf-8") as raw_file:
            pbar = tqdm(enumerate(raw_file), desc="Cleaning")
            for idx, line in pbar:
                pbar.set_postfix(
                    {
                        "pct_valid": f"{len(self.words) / (idx + 1):.2%}",
                        "n_valid": f"{len(self.words)/1000:.1f}K",
                    }
                )

                entry = json.loads(line)

                if is_redirect(entry):
                    self.redirects.append(
                        Redirect(from_word=entry["title"], to_word=entry["redirect"])
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

                entry["senses"] = self.filter_senses(entry["word"], entry["senses"])
                if not entry["senses"]:
                    continue

                self.words.append(Word.from_wiktionary(entry))

    def process_redirects(self) -> list[Redirect]:
        redirects_df = pd.DataFrame([json.loads(r.to_json()) for r in self.redirects])
        redirects_df = redirects_df.drop_duplicates(subset=["from_word"], keep="first")

        words_df = pd.DataFrame([w.word for w in self.words], columns=["word"])
        words_df = words_df.drop_duplicates(subset=["word"], keep="first")

        redirects_df = redirects_df.merge(
            words_df, left_on="to_word", right_on="word", how="inner"
        )

        return [
            Redirect(from_word=r.from_word, to_word=r.word)
            for r in redirects_df.itertuples()
        ]

    def export(self) -> None:
        self.redirects = self.process_redirects()

        client = connect("wordsea", host=MONGODB_URL)
        Word.drop_collection()
        Redirect.drop_collection()

        Word.objects.insert(self.words)
        Redirect.objects.insert(self.redirects)
        client.close()
