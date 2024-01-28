import os

DEFAULT_LLM_PROVIDER = os.getenv("ZRB_DEFAULT_LLM_PROVIDER", "ollama")
DEFAULT_OLLAMA_BASE_URL = os.getenv("ZRB_OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_OLLAMA_MODEL = os.getenv("ZRB_OLLAMA_DEFAULT_MODEL", "mistral")
DEFAULT_SYSTEM_PROMPT = os.getenv(
    "ZRB_DEFAULT_SYSTEM_PROMPT", "You are a helpful assistant"
)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
