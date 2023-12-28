from zrb.helper.string.conversion import to_boolean
import os

DEFAULT_OLLAMA_BASE_URL = os.getenv(
    'ZRB_OLLAMA_BASE_URL', 'http://localhost:11434'
)
DEFAULT_MODEL = os.getenv('ZRB_OLLAMA_DEFAULT_MODEL', 'mistral')
VERBOSE_EVAL = to_boolean(os.getenv('ZRB_OLLAMA_VERBOSE_EVAL', '0'))
