import json
import logging
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import requests
from jsonschema import ValidationError, validate

from wordsea.constants import LOGS_PATH, PromptModel

JSON_GRAMMAR = r"""root ::= ImagePrompt
ImagePrompt ::= "{"   ws   "\"explanation\":"   ws   string   ","   ws   "\"prompt\":"   ws   string   "}"
ImagePromptlist ::= "[]" | "["   ws   ImagePrompt   (","   ws   ImagePrompt)*   "]"
string ::= "\""   ([^"]*)   "\""
boolean ::= "true" | "false"
ws ::= [ \t\n]*
number ::= [0-9]+   "."?   [0-9]*
stringlist ::= "["   ws   "]" | "["   ws   string   (","   ws   string)*   ws   "]"
numberlist ::= "["   ws   "]" | "["   ws   string   (","   ws   number)*   ws   "]"
"""


@dataclass
class LLMParams:
    n_predict: int = 1024
    temperature: float = 0.7
    top_p: float = 1.0
    top_k: int = 100
    min_p: float = 0.02
    presence_penalty: float = 0.0
    dynatemp_range: float = 0.3
    frequency_penalty: float = 0.0
    repeat_penalty: float = 1.0
    penalize_nl: bool = False
    stop: list[str] = field(default_factory=lambda: ["</s>"])
    template: str = "{prompt}"

    def __post_init__(self) -> None:
        self.stop.append("}")


MistralNemoParams = LLMParams(template="[INST] {prompt} [/INST]")
Gemma2Params = LLMParams(
    template="<start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n",
    stop=["<end_of_turn>"],
)

OutputSchema = {
    "type": "object",
    "properties": {
        "explanation": {"type": "string"},
        "prompt": {"type": "string"},
    },
    "required": ["explanation", "prompt"],
    "additionalProperties": False,
}


class LlamaCppAPI:
    def __init__(self, url: str, model: PromptModel) -> None:
        self.base_url = url

        match model:
            case PromptModel.MISTRAL_NEMO:
                self.params = asdict(MistralNemoParams)
            case PromptModel.GEMMA2:
                self.params = asdict(Gemma2Params)
            case _:
                raise ValueError(f"Unknown model: {model}")

        self.template = self.params.pop("template")

    def health(self) -> bool:
        res = requests.get(f"{self.base_url}/health").json()
        return res["status"] == "ok"

    def log_error(self, path: Path, word: str, response: dict[str, Any]) -> None:
        with Path(path / "errors.jsonl", encoding="utf-8").open("a") as f:
            message = {"word": word, "response": response["content"]}
            f.write(json.dumps(message) + "\n")

    def generate(self, word: str, prompt: str) -> dict[str, Any]:
        prompt = self.template.format(prompt=prompt)
        res = requests.post(
            f"{self.base_url}/completion",
            json={
                "prompt": prompt,
                "grammar": JSON_GRAMMAR,
                **self.params,
            },
        ).json()
        res["content"] += "}"

        try:
            answer = json.loads(res["content"])
            validate(instance=answer, schema=OutputSchema)
        except json.JSONDecodeError:
            logging.error(f"Response was not valid JSON for {word}: {res['content']}")
            self.log_error(LOGS_PATH, word, res)

            return None
        except ValidationError:
            logging.error(f"Response did not match schema for {word}: {res['content']}")
            self.log_error(LOGS_PATH, word, res)

            return None
        else:
            answer["word"] = word

        return answer
