import os

DEFAULT_LLM_PROVIDER = os.getenv("ZRB_DEFAULT_LLM_PROVIDER", "ollama")
DEFAULT_CHAT_HISTORY_RETENTION = int(
    os.getenv("ZRB_DEFAULT_CHAT_HISTORY_RETENTION", "5")
)
DEFAULT_SYSTEM_PROMPT = os.getenv(
    "ZRB_DEFAULT_SYSTEM_PROMPT",
    "\n".join(
        [
            "Assistant is a large language model.",
            "Assistant is able to assist human in wide variaty of tasks.",
            "Assistant always validates and gives a correct information.",
            "Assistant never gives fake information or denies human requests at all cost.",  # noqa
            "Assistant uses available tools when needed.",
            "Assistant includes necessary details, reasoning, and explanation in the Final Answer.",  # noqa
        ]
    ),
)

DEFAULT_EMBEDDING_DB_DIR = os.getenv(
    "ZRB_DEFAULT_EMBEDDING_DB_DIR", os.path.join("~", ".zrb-embedding")
)

DEFAULT_CHAT_HISTORY_FILE_NAME = os.getenv(
    "ZRB_DEFAULT_CHAT_HISTORY_FILE", os.path.join("~", ".zrb-ollama-history.txt")
)


DEFAULT_OLLAMA_BASE_URL = os.getenv("ZRB_OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_OLLAMA_MODEL = os.getenv("ZRB_OLLAMA_DEFAULT_MODEL", "mistral:latest")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
