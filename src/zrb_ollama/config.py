import os
from zrb.helper.string.conversion import to_boolean

INIT_MODULE_STR = os.getenv("ZRB_OLLAMA_INIT_MODULES", "")
INIT_MODULES = (
    [
        init_module.strip()
        for init_module in INIT_MODULE_STR.split(":")
        if init_module.strip() != ""
    ]
    if INIT_MODULE_STR != ""
    else []
)

SHOULD_SHOW_SYSTEM_PROMPT = to_boolean(os.getenv(
    "ZRB_OLLAMA_SHOULD_SHOW_SYSTEM_PROMPT", "0"
))
INIT_SCRIPT_STR = os.getenv("ZRB_OLLAMA_INIT_SCRIPTS", "")
INIT_SCRIPTS = (
    [
        init_script.strip()
        for init_script in INIT_SCRIPT_STR.split(":")
        if init_script.strip() != ""
    ]
    if INIT_SCRIPT_STR != ""
    else []
)

LLM_MODEL = os.getenv("ZRB_OLLAMA_LLM_MODEL", "ollama/mistral:7b-instruct")
INTERACTIVE_ENABLED_TOOL_NAMES = [
    name.strip()
    for name in os.getenv(
        "ZRB_OLLAMA_INTERACTIVE_AGENT_TOOLS",
        "query_internet,open_web_page,run_shell_command",
    ).split(",")
]
CONVERSATION_LOG_PATH = os.path.expanduser(os.getenv(
    "ZRB_OLLAMA_CONVERSATION_LOG_PATH", "~/.zrb-ollama/history"
))
CONVERSATION_VECTOR_LOG_PATH = os.path.expanduser(os.getenv(
    "ZRB_OLLAMA_CONVERSATION_LOG_PATH", "~/.zrb-ollama/.vector"
))

RAG_EMBEDDING_MODEL = os.getenv(
    "ZRB_OLLAMA_RAG_EMBEDDING_MODEL", "ollama/nomic-embed-text"
)
RAG_CHUNK_SIZE = int(os.getenv("ZRB_OLLAMA_RAG_CHUNK_SIZE", "1024"))
RAG_OVERLAP = int(os.getenv("ZRB_OLLAMA_RAG_OVERLAP", "128"))
RAG_MAX_RESULT_COUNT = int(os.getenv("ZRB_OLLAMA_RAG_MAX_RESULT_COUNT", "5"))

DEFAULT_SYSTEM_PROMPT = os.getenv(
    "ZRB_OLLAMA_DEFAULT_SYSTEM_PROMPT",
    "You are a helpful assistant. You provide accurate and comprehensive answers.",
)


_default_system_message_template = """
{system_prompt}

You MUST ONLY respond in the following JSON format:

{response_format}

CRITICAL:
- Failure to use this exact format will result in an error.
- Never try to simulate the tool output.

Your goal is to provide a final answer by executing a series of actions and reasoning about the results.

VALID FUNCTION SIGNATURES
You can only use the following functions:

{function_signatures}

ERROR HANDLING
1. If you receive an error, read the error message carefully and identify the specific issue (e.g., missing arguments, invalid format).
2. Adjust your response accordingly and perform the review process again before resubmitting.

REMINDER: ALWAYS double-check your response format and function arguments before submitting.
""".strip()
DEFAULT_SYSTEM_MESSAGE_TEMPLATE = os.getenv(
    "ZRB_OLLAMA_DEFAULT_SYSTEM_MESSAGE_TEMPLATE", _default_system_message_template
)


DEFAULT_JSON_FIXER_SYSTEM_PROMPT = os.getenv(
    "ZRB_OLLAMA_DEFAULT_JSON_FIXER_SYSTEM_PROMPT",
    "You are a message fixer. You turn any message into JSON format. Your user is a LLM assistant that need to provide the correctly formatted message to serve the end user (human). If you think the LLM should end the conversation, make sure all necessary information for the human is included in the final_answer.",  # noqa
)

_default_json_fixer_system_message_template = """
{system_prompt}

You MUST FIX any message to STRICTLY USE the following JSON format:

{response_format}

VALID FUNCTION SIGNATURES
You can only use the following functions:
{function_signatures}
""".strip()
DEFAULT_JSON_FIXER_SYSTEM_MESSAGE_TEMPLATE = os.getenv(
    "ZRB_OLLAMA_DEFAULT_JSON_FIXER_SYSTEM_MESSAGE_TEMPLATE",
    _default_json_fixer_system_message_template,
)
