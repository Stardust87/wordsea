import json
from pathlib import Path
from typing import Any, Optional

import pandas as pd
from mongoengine import connect
from tqdm import tqdm

from wordsea.constants import MONGODB_URL
from wordsea.db.schema import Meaning, Redirect
from wordsea.dictionary.clean.constraints import (
    filter_nonalpha_examples,
    has_correct_word,
    is_language,
    is_redirect,
    is_vulgar,
    starts_with_number,
)
from wordsea.gen import parse_input_words


class WikiRawStream:
    def __init__(self, path: str, words_subset_path: Optional[str] = None):
        self.path = Path(path)
        self.words_subset = (
            {word: True for word in parse_input_words([words_subset_path])}
            if words_subset_path
            else {}
        )

        self.redirects: list[Redirect] = []
        self.meanings: list[Meaning] = []

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

    def process(self) -> None:
        with self.path.open(encoding="utf-8") as raw_file:
            pbar = tqdm(enumerate(raw_file), desc="Cleaning")
            for idx, line in pbar:
                pbar.set_postfix(
                    {
                        "pct_valid": f"{len(self.meanings) / (idx + 1):.2%}",
                        "n_valid": f"{len(self.meanings)/1000:.1f}K",
                    }
                )
                entry = json.loads(line)

                if self.words_subset and entry["word"] not in self.words_subset:
                    continue
                if is_redirect(entry):
                    self.redirects.append(
                        Redirect(from_word=entry["title"], to_word=entry["redirect"])
                    )
                    continue
                if not is_language(entry):
                    continue
                if not has_correct_word(entry):
                    continue
                if is_vulgar(entry):
                    continue

                entry["senses"] = self.filter_senses(entry["word"], entry["senses"])
                if not entry["senses"]:
                    continue

                self.meanings.append(Meaning.from_wiktionary(entry))

    def process_redirects(self) -> list[Redirect]:
        redirects_df = pd.DataFrame(
            [json.loads(r.to_json(ensure_ascii=False)) for r in self.redirects]
        )
        redirects_df = redirects_df.drop_duplicates(subset=["from_word"], keep="first")

        meanings_df = pd.DataFrame([w.word for w in self.meanings], columns=["word"])
        meanings_df = meanings_df.drop_duplicates(subset=["word"], keep="first")

        redirects_df = redirects_df.merge(
            meanings_df, left_on="to_word", right_on="word", how="inner"
        )

        return [
            Redirect(from_word=r.from_word, to_word=r.word)
            for r in redirects_df.itertuples()
        ]

    def export(self) -> None:
        self.redirects = self.process_redirects()

        client = connect("wordsea", host=MONGODB_URL)
        Meaning.drop_collection()
        Redirect.drop_collection()

        Meaning.objects.insert(self.meanings)
        Redirect.objects.insert(self.redirects)
        client.close()
