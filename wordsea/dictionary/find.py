import logging
import json
from pathlib import Path

import pandas as pd
from tqdm import tqdm


logging.basicConfig(
    format="%(levelname)s - %(message)s",
    level=logging.WARNING,
)


def find_words(
    words: list[str],
    path: Path,
):
    info_path = path.parent / (path.stem + "-info.csv")
    info = pd.read_csv(info_path)

    words_info = info[info["word"].isin(words)]
    not_found = set(words) - set(words_info.word.unique().tolist())
    if not_found:
        logging.warning(f"The following words were not found: {', '.join(not_found)}")

    line_indices = sorted(words_info.id.tolist())
    if not line_indices:
        raise ValueError("No definitions found.")

    matched = []
    with open(path, encoding="utf-8") as f:
        for idx, line in enumerate(tqdm(f)):
            if idx == line_indices[0]:
                matched.append(line)
                line_indices.pop(0)
                if not line_indices:
                    break

    words_info.loc[:, ["data"]] = matched
    found_words = {
        word: [json.loads(line) for line in group.data]
        for word, group in words_info.groupby("word")
    }

    return found_words
