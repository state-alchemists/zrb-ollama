import os

_current_dir = os.path.dirname(__file__)
with open(os.path.join(_current_dir, "system-prompt.txt")) as f:
    _default_system_prompt = f.read()
SYSTEM_PROMPT = os.getenv("ZRB_SYSTEM_PROMPT", _default_system_prompt)

with open(os.path.join(_current_dir, "factory", "prompt", "react-prompt.txt")) as f:
    _default_react_prompt = f.read()
REACT_PROMPT = os.getenv("ZRB_REACT_PROMPT", _default_react_prompt)

LLM_PROVIDER = os.getenv("ZRB_LLM_PROVIDER", "ollama")
CHAT_HISTORY_RETENTION = int(os.getenv("ZRB_CHAT_HISTORY_RETENTION", "5"))

MAX_SEARCH_RESULT = int(os.getenv("ZRB_MAX_SEARCH_RESULT", "3"))
MAX_SEARCH_CHAR_LENGTH = int(os.getenv("ZRB_MAX_SEARCH_CHAR_LENGTH", "3000"))

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
OLLAMA_EMBEDDING_MODEL = os.getenv("ZRB_OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo-instruct")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "")
if OPENAI_API_BASE.strip() == "":
    OPENAI_API_BASE = None

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

AWS_BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-v2")
