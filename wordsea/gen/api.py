import json
import logging
from dataclasses import asdict, dataclass, field
from typing import Any

import requests
from jsonschema import ValidationError, validate

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
    temperature: float = 0.8
    top_p: float = 1.0
    top_k: int = 40
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


MixtralParams = LLMParams(
    template="[INST] {prompt} [/INST]", dynatemp_range=0.5, temperature=0.7
)
MistralParams = LLMParams(template="[INST] {prompt} [/INST]")
YiParams = LLMParams(
    template="<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant"
)
QwenParams = LLMParams(
    template="<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant",
    dynatemp_range=0.2,
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
    def __init__(self, url: str, model: str = "mixtral") -> None:
        self.base_url = url

        match model:
            case "mixtral":
                self.params = asdict(MixtralParams)
            case "mistral":
                self.params = asdict(MistralParams)
            case "yi":
                self.params = asdict(YiParams)
            case "qwen":
                self.params = asdict(QwenParams)
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
