from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Example:
    text: str
    ref: Optional[str] = None
    type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Example":
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

    def __post_init__(self) -> None:
        if self.aliases is None:
            self.aliases = set()

    @classmethod
    def from_dict(cls, id: int, data: dict[str, Any]) -> "Entry":
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

    def to_dict(self) -> dict[str, Any]:
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
