import sys

from zrb.helper.accessories.color import colored

from .builtin.install import install
from .config import DEFAULT_LLM_PROVIDER
from .factory.tool.bash_repl import bash_repl_tool_factory
from .factory.tool.python_repl import python_repl_tool_factory
from .factory.tool.search import search_tool_factory
from .task.prompt_task import PromptTask


def prompt():
    if len(sys.argv) > 1:
        input_prompt = " ".join(sys.argv[1:])
        _exec_prompt(input_prompt)
        return
    _print_all_instructions()
    is_multiline = False
    lines = []
    while True:
        line = _get_line(show_input_prompt=not is_multiline)
        if is_multiline:
            if line.lower() == '/end':
                is_multiline = False
                input_prompt = "\n".join(lines)
                _exec_prompt(input_prompt)
                continue
            lines.append(line)
            continue
        if line.lower() in ['/bye', '/quit', '/q', '/exit']:
            return
        if line.lower() in ['/?', '/help']:
            _print_all_instructions()
            continue
        if line.lower() in ['/multi', '/multiline']:
            is_multiline = True
            lines = []
            continue
        _exec_prompt(line)


def _get_line(show_input_prompt: bool) -> str:
    if show_input_prompt:
        _print_dark("Enter your input:")
    return sys.stdin.readline().strip()


def _exec_prompt(input_prompt: str):
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


def _print_all_instructions():
    _print_instruction("/?", "Show help")
    _print_instruction("/bye", "Quit")
    _print_instruction("/multi", "Start multiline mode")
    _print_instruction("/end", "Stop multiline mode")


def _print_instruction(instruction: str, description: str):
    print("\t".join([
        colored(f' {instruction}', color='yellow', attrs=["dark"]),
        colored(description, attrs=["dark"])
    ]))


def _print_dark(text: str):
    print(colored(text, attrs=["dark"]))

