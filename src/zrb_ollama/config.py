import os

DEFAULT_LLM_PROVIDER = os.getenv("ZRB_DEFAULT_LLM_PROVIDER", "ollama")
DEFAULT_CHAT_HISTORY_RETENTION = int(
    os.getenv("ZRB_DEFAULT_CHAT_HISTORY_RETENTION", "3")
)
DEFAULT_SYSTEM_PROMPT = os.getenv(
    "ZRB_DEFAULT_SYSTEM_PROMPT",
    "\n".join(
        [
            "You are a helpful assistant."
            "You always validate and give a correct information.",
            "You never give fake information at all cost.",
            "You also include necessary details, reasoning, and explanation in your Final Answer.",  # noqa
        ]
    ),
)

DEFAULT_OLLAMA_BASE_URL = os.getenv("ZRB_OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_OLLAMA_MODEL = os.getenv("ZRB_OLLAMA_DEFAULT_MODEL", "mistral:latest")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
