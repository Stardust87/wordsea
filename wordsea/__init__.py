import subprocess
from enum import Enum


class Tools(str, Enum):
    CLEAN = "clean"


def main():
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
        case _:
            raise ValueError(
                f"tool not supported: {sys.argv[1]}, choose from {[tool.value for tool in Tools]}"
            )
