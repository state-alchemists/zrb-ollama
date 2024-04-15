from typing import List

from langchain_community.llms.ollama import Ollama
from langchain_core.language_models import BaseLanguageModel

from ...config import OLLAMA_BASE_URL, OLLAMA_MODEL
from ...task.any_prompt_task import AnyPromptTask
from ..schema import LLMFactory


def ollama_llm_factory(
    base_url: str = OLLAMA_BASE_URL,
    model: str = OLLAMA_MODEL,
    mirostat: str | int | None = None,
    mirostat_eta: str | float | None = None,
    mirostat_tau: str | float | None = None,
    num_ctx: str | int | None = None,
    num_gpu: str | int | None = None,
    num_thread: str | int | None = None,
    repeat_last_n: str | int | None = None,
    repeat_penalty: str | float | None = None,
    temperature: str | float | None = 0.0,
    stop: List[str] | None = None,
    tfs_z: str | float | None = None,
    top_k: str | int | None = None,
    top_p: str | int | None = None,
) -> LLMFactory:
    def create_ollama_llm(task: AnyPromptTask) -> BaseLanguageModel:
        return Ollama(
            base_url=task.render_str(base_url),
            model=task.render_str(model),
            mirostat=task.render_any(mirostat),
            mirostat_eta=task.render_any(mirostat_eta),
            mirostat_tau=task.render_any(mirostat_tau),
            num_ctx=task.render_any(num_ctx),
            num_gpu=task.render_any(num_gpu),
            num_thread=task.render_any(num_thread),
            repeat_last_n=task.render_any(repeat_last_n),
            repeat_penalty=task.render_any(repeat_penalty),
            temperature=task.render_any(temperature),
            stop=task.render_any(stop),
            tfs_z=task.render_any(tfs_z),
            top_k=task.render_any(top_k),
            top_p=task.render_any(top_p),
            callback_manager=task.get_callback_manager(),
        )

    return create_ollama_llm
