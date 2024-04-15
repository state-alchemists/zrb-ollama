import os

LLM_PROVIDER = os.getenv("ZRB_LLM_PROVIDER", "ollama")
CHAT_HISTORY_RETENTION = int(os.getenv("ZRB_CHAT_HISTORY_RETENTION", "5"))
SYSTEM_PROMPT = os.getenv(
    "ZRB_SYSTEM_PROMPT",
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

EMBEDDING_DB_DIR = os.getenv(
    "ZRB_EMBEDDING_DB_DIR",
    os.path.expanduser(os.path.join("~", ".zrb-embedding"))
)

CHAT_HISTORY_FILE_NAME = os.getenv(
    "ZRB_CHAT_HISTORY_FILE",
    os.path.expanduser(os.path.join("~", ".zrb-ollama-history.txt"))
)

DOCUMENT_DIRS = os.getenv("ZRB_DOCUMENT_DIRS", "")

OLLAMA_BASE_URL = os.getenv("ZRB_OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("ZRB_OLLAMA_MODEL", "mistral:latest")
OLLAMA_EMBEDDING_MODEL = os.getenv("ZRB_OLLAMA_EMBEDDING_MODEL", "mistral:latest")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME", "us-east-1")

BEDROCK_MODEL = os.getenv("ZRB_BEDROCK_MODEL", "anthropic.claude-v2")
