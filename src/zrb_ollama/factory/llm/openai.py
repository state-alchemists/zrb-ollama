from langchain_core.language_models import BaseLanguageModel
from langchain_openai import ChatOpenAI

from zrb_ollama.config import OPENAI_API_KEY
from zrb_ollama.factory.schema import LLMFactory
from zrb_ollama.task.any_prompt_task import AnyPromptTask


def openai_llm_factory(
    api_key=OPENAI_API_KEY,
    temperature=0,
) -> LLMFactory:
    def create_openai_llm(task: AnyPromptTask) -> BaseLanguageModel:
        return ChatOpenAI(
            api_key=task.render_str(api_key),
            temperature=task.render_int(temperature),
            streaming=True,
            callback_manager=task.get_callback_manager(),
        )

    return create_openai_llm
