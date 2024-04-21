from typing import Any, Dict

from langchain_core.language_models import BaseLanguageModel
from langchain_openai import OpenAI

from ...config import OPENAI_API_KEY, OPENAI_API_BASE, OPENAI_MODEL
from ...task.any_prompt_task import AnyPromptTask
from ..schema import LLMFactory


def openai_llm_factory(
    model: str = OPENAI_MODEL,
    temperature: str | float = 0.0,
    max_tokens: str | int = 256,
    top_p: str | float = 1.0,
    frequency_penalty: str | float = 0.0,
    presence_penalty: str | float = 0.0,
    n: str | int = 1,
    best_of: str | int = 1,
    model_kwargs: Dict[str, Any] = {},
    api_key: str | None = OPENAI_API_KEY,
    base_url: str | None = OPENAI_API_BASE,
) -> LLMFactory:
    def create_openai_llm(task: AnyPromptTask) -> BaseLanguageModel:
        return OpenAI(
            model=task.render_str(model),
            temperature=task.render_float(temperature),
            max_tokens=task.render_int(max_tokens),
            top_p=task.render_float(top_p),
            frequency_penalty=task.render_float(frequency_penalty),
            presence_penalty=task.render_float(presence_penalty),
            n=task.render_int(n),
            best_of=task.render_int(best_of),
            model_kwargs={
                task.render_str(key): task.render_any(value)
                for key, value in model_kwargs.items()
            },
            api_key=task.render_any(api_key),
            base_url=task.render_any(base_url),
            streaming=True,
            callback_manager=task.get_callback_manager(),
        )
    return create_openai_llm
