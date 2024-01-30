import sys

from zrb.helper.accessories.color import colored

from .builtin.install import install
from .config import DEFAULT_LLM_PROVIDER
from .factory.tool.bash_repl import bash_repl_tool_factory
from .factory.tool.python_repl import python_repl_tool_factory
from .factory.tool.search import search_tool_factory
from .task.prompt_task import PromptTask


def prompt():
    input_prompt = _get_input_prompt()
    prompt_task = PromptTask(
        name="prompt",
        icon="🦙",
        color="light_green",
        input_prompt=input_prompt,
        tool_factories=[
            search_tool_factory(),
            bash_repl_tool_factory(),
            python_repl_tool_factory(),
        ],
    )
    if DEFAULT_LLM_PROVIDER == "ollama":
        prompt_task.add_upstream(install)
    prompt_fn = prompt_task.to_function()
    prompt_fn()


def _get_input_prompt():
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:])
    print(colored("Enter your input (end with an empty line):", attrs=["dark"]))
    input_lines = []
    while True:
        line = sys.stdin.readline()
        if line == "\n":
            break
        input_lines.append(line)
    print(colored("Processing your input...", attrs=["dark"]))
    return "".join(input_lines).strip()
