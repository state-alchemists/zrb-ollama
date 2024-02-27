import sys

from zrb.helper.accessories.color import colored

from .builtin.install import install
from .config import DEFAULT_LLM_PROVIDER
from .factory.tool.bash_repl import bash_repl_tool_factory
from .factory.tool.python_repl import python_repl_tool_factory
from .factory.tool.search import search_tool_factory
from .task.prompt_task import PromptTask


def prompt():
    while True:
        _print_dark("/bye to quit")
        _print_dark(
            "Enter your input, end with two consecutive enters (i.e. \\n\\n):"
        )
        input_prompt = _get_input_prompt()
        if input_prompt.strip() == "/bye":
            return
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
        _print_dark("Processing your input...")
        prompt_fn = prompt_task.to_function()
        prompt_fn()


def _print_dark(text: str):
    print(colored(text, attrs=["dark"]))


def _get_input_prompt():
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:])
    input_lines = []
    while True:
        line = sys.stdin.readline()
        if line == "\n":
            break
        input_lines.append(line)
    return "".join(input_lines).strip()
