import sys

from zrb.helper.accessories.color import colored

from .builtin.install import install_ollama
from .config import LLM_PROVIDER
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
            if line.lower() == "/end":
                is_multiline = False
                input_prompt = "\n".join(lines)
                _exec_prompt(input_prompt)
                continue
            lines.append(line)
            continue
        if line.lower() in ["/bye", "/quit", "/q", "/exit"]:
            return
        if line.lower() in ["/?", "/help"]:
            _print_all_instructions()
            continue
        if line.lower() in ["/multi", "/multiline"]:
            is_multiline = True
            lines = []
            continue
        if line.lower() in ["/clear", "/reset"]:
            _clear_history()
            continue
        _exec_prompt(line)


def _get_line(show_input_prompt: bool) -> str:
    if show_input_prompt:
        _print_dark("Enter your input:")
    return sys.stdin.readline().strip()


def _clear_history():
    prompt_task = _create_prompt_task("")
    prompt_task.clear_history()


def _exec_prompt(input_prompt: str):
    prompt_task = _create_prompt_task(input_prompt)
    _print_dark("Processing your input...")
    prompt_fn = prompt_task.to_function(show_done_info=False)
    prompt_fn()


def _create_prompt_task(input_prompt: str) -> PromptTask:
    prompt_task = PromptTask(
        name="prompt",
        icon="🦙",
        color="light_green",
        input_prompt=input_prompt,
    )
    if LLM_PROVIDER == "ollama":
        prompt_task.add_upstream(install_ollama)
    return prompt_task


def _print_all_instructions():
    _print_instruction("/?", "Show help")
    _print_instruction("/bye", "Quit")
    _print_instruction("/multi", "Start multiline mode")
    _print_instruction("/end", "Stop multiline mode")
    _print_instruction("/clear", "Clear history")


def _print_instruction(instruction: str, description: str):
    print(
        "\t".join(
            [
                colored(f" {instruction}", color="yellow", attrs=["dark"]),
                colored(description, attrs=["dark"]),
            ]
        )
    )


def _print_dark(text: str):
    print(colored(text, attrs=["dark"]))
