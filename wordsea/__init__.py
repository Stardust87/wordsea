import subprocess
from enum import Enum


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
