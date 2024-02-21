from typing import Any, ClassVar, Optional

from mongoengine import (
    DictField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
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
    ipa = StringField()
    audio = StringField()
    derived_from = StringField()

    @staticmethod
    def extract_phonetics(data: dict[str, Any]) -> tuple[Optional[str], Optional[str]]:
        """Extract phonetic transcription and audio URL from Wiktionary data."""

        if "sounds" not in data:
            return None, None

        preferred_origins = ["US", "General-American", "UK"]
        all_ipas = [sound for sound in data["sounds"] if "ipa" in sound]
        if not all_ipas:
            ipa = None
        else:
            preffered_ipas = [
                sound
                for sound in all_ipas
                if "tags" in sound and sound["tags"][0] in preferred_origins
            ]
            if not preffered_ipas:
                ipa = all_ipas[0]["ipa"]
            else:
                preffered_ipas = sorted(
                    preffered_ipas, key=lambda x: preferred_origins.index(x["tags"][0])
                )
                ipa = preffered_ipas[0]["ipa"]

        all_audios: list[str] = [
            sound["mp3_url"] for sound in data["sounds"] if "mp3_url" in sound
        ]
        if all_audios:
            audio = all_audios[0]
        else:
            audio = None

        return ipa, audio

    @classmethod
    def from_wiktionary(cls, data: dict[str, Any]) -> "Meaning":
        word = data["word"]
        pos = data["pos"]

        senses = []
        for sense in data["senses"]:
            gloss = sense["glosses"][0]
            raw_gloss = sense["raw_glosses"][0] if "raw_glosses" in sense else None
            examples = [
                Example.from_wiktionary(ex)
                for ex in sense.get("examples", [])
                if len(ex["text"]) < 240
            ]
            senses.append(Sense(gloss=gloss, raw_gloss=raw_gloss, examples=examples))

        forms = {}
        for form in data.get("forms", []):
            if "tags" not in form:
                continue

            for form_type, tags in FORMS_TYPES.items():
                if tags == set(form["tags"]):
                    forms[form_type] = form["form"]
                    break

        ipa, audio = cls.extract_phonetics(data)
        derived_from = data.get("derived_from", None)

        return cls(
            word=word,
            pos=pos,
            senses=senses,
            forms=forms,
            ipa=ipa,
            audio=audio,
            derived_from=derived_from,
        )


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
    image = EmbeddedDocumentField(Image)
    image_model = StringField()
