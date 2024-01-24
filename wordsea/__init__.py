import os
import subprocess
from enum import Enum
from pathlib import Path

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
LLAMACPP_URL = os.getenv("LLAMACPP_URL", "http://localhost:8080")
LOG_DIR = Path(os.getenv("LOG_DIR", "logs"))
LOG_DIR.mkdir(exist_ok=True, parents=True)
MINDICT_FILE = Path(os.getenv("MINDICT_FILE", "raw-wiktextract-data-minimal.json"))


class Tools(str, Enum):
    CLEAN = "clean"
    FIND = "find"
    GENERATE = "generate"
    IMAGINE = "imagine"


def main() -> None:
    import sys

    toolargs = sys.argv[2:]
    match sys.argv[1]:
        case Tools.CLEAN:
            subprocess.run(
                [
                    f"wordsea-{Tools.CLEAN.value}",
                    *toolargs,
                ]
            )
        case Tools.FIND:
            subprocess.run(
                [
                    f"wordsea-{Tools.FIND.value}",
                    *toolargs,
                ]
            )
        case Tools.GENERATE:
            subprocess.run(
                [
                    f"wordsea-{Tools.GENERATE.value}",
                    *toolargs,
                ]
            )
        case Tools.IMAGINE:
            subprocess.run(
                [
                    f"wordsea-{Tools.IMAGINE.value}",
                    *toolargs,
                ]
            )
        case _:
            raise ValueError(
                f"tool not supported: {sys.argv[1]}, choose from {[tool.value for tool in Tools]}"
            )
