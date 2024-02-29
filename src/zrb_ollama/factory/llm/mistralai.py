from langchain_core.language_models import BaseLanguageModel
from langchain_mistralai import ChatMistralAI

from zrb_ollama.config import MISTRAL_API_KEY
from zrb_ollama.factory.schema import LLMFactory
from zrb_ollama.task.any_prompt_task import AnyPromptTask


def mistralai_llm_factory(
    api_key: str | None = MISTRAL_API_KEY,
    model: str = "mistral-large-2402",
    temperature: str | float = 0.0,
    max_tokens: str | int = 256,
    top_p: str | float = 1.0,
    safe_mode: str | bool = False,
) -> LLMFactory:
    def create_mistralai_llm(task: AnyPromptTask) -> BaseLanguageModel:
        return ChatMistralAI(
            model=task.render_str(model),
            temperature=task.render_float(temperature),
            max_tokens=task.render_int(max_tokens),
            top_p=task.render_float(top_p),
            api_key=task.render_any(api_key),
            safe_mode=task.render_bool(safe_mode),
            callback_manager=task.get_callback_manager(),
        )

    return create_mistralai_llm
