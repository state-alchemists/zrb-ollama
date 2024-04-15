from langchain_core.embeddings import Embeddings

from ..bedrock.helper import create_bedrock_client
from ..config import (
    LLM_PROVIDER,
    OLLAMA_BASE_URL,
    OLLAMA_EMBEDDING_MODEL,
    OPENAI_API_KEY,
)


def get_default_rag_embedding(llm_provider: str = LLM_PROVIDER) -> Embeddings:
    if llm_provider == "openai":
        from langchain_openai import OpenAIEmbeddings

        return OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    if llm_provider == "bedrock":
        from langchain_community.embeddings.bedrock import BedrockEmbeddings

        bedrock_client = create_bedrock_client()
        return BedrockEmbeddings(client=bedrock_client)
    from langchain_community.embeddings.ollama import OllamaEmbeddings

    return OllamaEmbeddings(
        base_url=OLLAMA_BASE_URL,
        model=OLLAMA_EMBEDDING_MODEL,
    )
