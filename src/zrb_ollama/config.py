import os

INIT_MODULE_STR = os.getenv("ZRB_OLLAMA_INIT_MODULES", "")
INIT_MODULES = [
    init_module.strip()
    for init_module in INIT_MODULE_STR.split(":") if init_module.strip() != ""
] if INIT_MODULE_STR != "" else []

INIT_SCRIPT_STR = os.getenv("ZRB_OLLAMA_INIT_SCRIPTS", "")
INIT_SCRIPTS = [
    init_script.strip()
    for init_script in INIT_SCRIPT_STR.split(":") if init_script.strip() != ""
] if INIT_SCRIPT_STR != "" else []

LLM_MODEL = os.getenv("ZRB_OLLAMA_LLM_MODEL", "ollama/mistral:7b-instruct")
INTERACTIVE_ENABLED_TOOL_NAMES = [
    name.strip()
    for name in os.getenv(
        "ZRB_OLLAMA_INTERACTIVE_AGENT_TOOLS",
        "query_internet,open_web_page,run_shell_command"
    ).split(",")
]

RAG_EMBEDDING_MODEL = os.getenv(
    "ZRB_OLLAMA_RAG_EMBEDDING_MODEL", "ollama/nomic-embed-text"
)
RAG_CHUNK_SIZE = int(os.getenv("ZRB_OLLAMA_RAG_CHUNK_SIZE", "1024"))
RAG_OVERLAP = int(os.getenv("ZRB_OLLAMA_RAG_OVERLAP", "128"))
RAG_MAX_RESULT_COUNT = int(os.getenv("ZRB_OLLAMA_RAG_MAX_RESULT_COUNT", "5"))

DEFAULT_SYSTEM_PROMPT = os.getenv(
    "ZRB_OLLAMA_DEFAULT_SYSTEM_PROMPT",
    "You are a helpful assistant. You provide accurate and comprehensive answers."
)

_default_system_message_template = """
{system_prompt}

Your responses MUST ALWAYS STRICTLY follow this JSON format structure:

{response_format}

CRITICAL: Failure to use this exact format will result in an error.

Your goal is to find an accurate final_answer through a series of thoughts and actions.

FUNCTION RULES:
1. Only use functions listed in the FUNCTION SCHEMA below.
2. Provide ALL required arguments for each function.
3. Do not include extra or invalid arguments.
4. Only use finish_conversation when you have the final_answer or it's impossible to find one.

FUNCTION SCHEMA:

{function_signatures}

ERROR HANDLING:
If you receive an error:
1. Read the error message carefully.
2. Identify the specific issue (e.g., missing arguments, invalid format).
3. Adjust your response accordingly.
4. Perform the review process again before resubmitting.

REMINDER: ALWAYS double-check your response format and function arguments before submitting.
""".strip()
DEFAULT_SYSTEM_MESSAGE_TEMPLATE = os.getenv(
    "ZRB_OLLAMA_DEFAULT_SYSTEM_MESSAGE_TEMPLATE", _default_system_message_template
)
