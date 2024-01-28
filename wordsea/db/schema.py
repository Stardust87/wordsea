from typing import Any, ClassVar

from mongoengine import (
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    FileField,
    ListField,
    StringField,
)


class Example(EmbeddedDocument):
    text = StringField(required=True)
    ref = StringField()
    type = StringField()

    @classmethod
    def from_wiktionary(cls, data: dict[str, Any]) -> "Example":
        return cls(
            text=data["text"],
            ref=data.get("ref"),
            type=data.get("type"),
        )


class Sense(EmbeddedDocument):
    gloss = StringField(required=True)
    raw_gloss = StringField()
    examples = ListField(EmbeddedDocumentField("Example"))


class Word(Document):
    meta: ClassVar[dict] = {"collection": "words"}
    word = StringField(required=True)
    pos = StringField(required=True)
    senses = ListField(EmbeddedDocumentField("Sense"))

    @classmethod
    def from_wiktionary(cls, data: dict[str, Any]) -> "Word":
        word = data["word"]
        pos = data["pos"]

        senses = []
        for sense in data["senses"]:
            gloss = sense["glosses"][0]
            raw_gloss = sense["raw_glosses"][0] if "raw_glosses" in sense else None
            examples = [Example.from_wiktionary(ex) for ex in sense.get("examples", [])]
            senses.append(Sense(gloss=gloss, raw_gloss=raw_gloss, examples=examples))

        return cls(word=word, pos=pos, senses=senses)


class Redirect(Document):
    meta: ClassVar[dict] = {"collection": "redirects"}
    from_word = StringField(required=True)
    to_word = StringField(required=True)


class Image(EmbeddedDocument):
    data = FileField()


class Mnemonic(Document):
    meta: ClassVar[dict] = {"collection": "mnemonics"}
    word = StringField(required=True)
    explanation = StringField(required=True)
    prompt = StringField(required=True)
    language_model = StringField(required=True)
    images = EmbeddedDocumentListField(Image)
    image_model = StringField()
