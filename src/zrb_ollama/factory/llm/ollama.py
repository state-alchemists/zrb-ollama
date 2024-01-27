from langchain_community.chat_models import ChatOllama
from langchain_core.language_models import BaseLanguageModel

from zrb_ollama.config import DEFAULT_OLLAMA_BASE_URL, DEFAULT_OLLAMA_MODEL
from zrb_ollama.factory.schema import LLMFactory
from zrb_ollama.task.any_prompt_task import AnyPromptTask


def ollama_llm_factory(
    base_url=DEFAULT_OLLAMA_BASE_URL,
    model=DEFAULT_OLLAMA_MODEL,
    temperature=0,
) -> LLMFactory:
    def create_ollama_llm(task: AnyPromptTask) -> BaseLanguageModel:
        return ChatOllama(
            base_url=task.render_str(base_url),
            model=task.render_str(model),
            temperature=task.render_int(temperature),
            callback_manager=task.get_callback_manager(),
        )

    return create_ollama_llm
