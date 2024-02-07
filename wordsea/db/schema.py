from typing import Any, ClassVar

from mongoengine import (
    DictField,
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
            text=data["text"].replace("&#32;", ""),
            ref=data.get("ref"),
            type=data.get("type"),
        )


class Sense(EmbeddedDocument):
    gloss = StringField(required=True)
    raw_gloss = StringField()
    examples = ListField(EmbeddedDocumentField("Example"))


FORMS_TYPES = {
    "third_person": {"present", "singular", "third-person"},
    "present_participle": {"present", "participle"},
    "past_participle": {"past", "participle"},
    "comparative": {"comparative"},
    "superlative": {"superlative"},
    "plural": {"plural"},
}


class Meaning(Document):
    meta: ClassVar[dict] = {"collection": "meanings"}
    word = StringField(required=True)
    pos = StringField(required=True)
    senses = ListField(EmbeddedDocumentField("Sense"))
    forms = DictField()

    @classmethod
    def from_wiktionary(cls, data: dict[str, Any]) -> "Meaning":
        word = data["word"]
        pos = data["pos"]

        senses = []
        for sense in data["senses"]:
            gloss = sense["glosses"][0]
            raw_gloss = sense["raw_glosses"][0] if "raw_glosses" in sense else None
            examples = [Example.from_wiktionary(ex) for ex in sense.get("examples", [])]
            senses.append(Sense(gloss=gloss, raw_gloss=raw_gloss, examples=examples))

        forms = {}
        for form in data.get("forms", []):
            if "tags" not in form:
                continue

            for form_type, tags in FORMS_TYPES.items():
                if tags == set(form["tags"]):
                    forms[form_type] = form["form"]
                    break

        return cls(word=word, pos=pos, senses=senses, forms=forms)


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
