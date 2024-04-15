from ...config import LLM_PROVIDER
from ..schema import LLMFactory


def default_llm_factory(llm_provider: str = LLM_PROVIDER) -> LLMFactory:
    if llm_provider == "openai":
        from .openai import openai_llm_factory

        return openai_llm_factory()
    if llm_provider == "bedrock":
        from .bedrock import bedrock_llm_factory

        return bedrock_llm_factory()
    from .ollama import ollama_llm_factory

    return ollama_llm_factory()
