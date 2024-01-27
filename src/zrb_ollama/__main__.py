import sys

from .builtin.install import install
from .config import DEFAULT_LLM_PROVIDER
from .task.prompt_task import PromptTask


def prompt():
    input_prompt = _get_input_prompt()
    prompt_task = PromptTask(
        name="prompt",
        icon="🦙",
        color="light_green",
        input_prompt=input_prompt,
    )
    if DEFAULT_LLM_PROVIDER == "ollama":
        prompt_task.add_upstream(install)
    prompt_fn = prompt_task.to_function()
    prompt_fn()


def _get_input_prompt():
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:])
    return "Tell me some random fun facts"
