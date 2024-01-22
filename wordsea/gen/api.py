import json
import logging
from dataclasses import asdict, dataclass, field
from typing import Any

import requests
from jsonschema import ValidationError, validate

logging.basicConfig(
    format="%(levelname)s - %(message)s",
    level=logging.ERROR,
)

JSON_GRAMMAR = r"""root   ::= object
value  ::= object | array | string | number | ("true" | "false" | "null") ws

object ::=
"{" ws (
            string ":" ws value
    ("," ws string ":" ws value)*
)? "}" ws

array  ::=
"[" ws (
            value
    ("," ws value)*
)? "]" ws

string ::=
"\"" (
    [^"\\] |
    "\\" (["\\/bfnrt] | "u" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F]) # escapes
)* "\"" ws

number ::= ("-"? ([0-9] | [1-9] [0-9]*)) ("." [0-9]+)? ([eE] [-+]? [0-9]+)? ws

# Optional space: by convention, applied in this grammar after literal chars when allowed
ws ::= ([ \t\n] ws)?"""


@dataclass
class LLMParams:
    n_predict: int = 1024
    temperature: float = 0.7
    top_p: float = 1.0
    top_k: int = 40
    min_p: float = 0.02
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    repeat_penalty: float = 1.0
    penalize_nl: bool = False
    stop: list[str] = field(default_factory=lambda: ["</s>"])
    template: str = "{prompt}"

    def __post_init__(self) -> None:
        self.stop.append("}")


MixtralParams = LLMParams(template="[INST] {prompt} [/INST]")
MistralParams = LLMParams(template="[INST] {prompt} [/INST]")

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
    def __init__(self, url: str, model: str = "mixtral") -> None:
        self.base_url = url

        match model:
            case "mixtral":
                self.params = asdict(MixtralParams)
            case "mistral":
                self.params = asdict(MistralParams)
            case _:
                raise ValueError(f"Unknown model: {model}")

        self.template = self.params.pop("template")

    def health(self) -> bool:
        res = requests.get(f"{self.base_url}/health").json()
        return res["status"] == "ok"

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
            return None
        except ValidationError:
            logging.error(f"Response did not match schema for {word}: {res['content']}")
            return None
        else:
            answer["word"] = word

        return answer
