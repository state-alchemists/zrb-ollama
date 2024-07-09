import sys

from zrb.helper.accessories.color import colored
from .agent import Agent
from .tools import run_shell_command, query_internet


def prompt():
    model = "ollama/mistral:7b-instruct"
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        _exec_prompt(model, user_input)
        return
    _print_all_instructions()
    is_multiline = False
    lines = []
    while True:
        try:
            line = _get_line(show_input_prompt=not is_multiline)
        except KeyboardInterrupt:
            _print_dark("\nBye")
            return
        if is_multiline:
            if line.lower() == "/end":
                is_multiline = False
                user_input = "\n".join(lines)
                _exec_prompt(model, user_input)
                continue
            lines.append(line)
            continue
        if line.lower() in ["/bye", "/quit", "/q", "/exit"]:
            _print_dark("Bye")
            return
        if line.lower() in ["/?", "/help"]:
            _print_all_instructions()
            continue
        if line.lower() in ["/multi", "/multiline"]:
            is_multiline = True
            lines = []
            continue
        if line.lower() == "/llm":
            _print_dark(f"LLM: {model}")
            continue
        if line.lower().startswith("/llm"):
            model = line[len("/llm"):].strip()
            continue
        # Run the task
        user_input = line
        _exec_prompt(model, user_input)


def _get_line(show_input_prompt: bool) -> str:
    if show_input_prompt:
        _print_dark("Enter your input:")
    return sys.stdin.readline().strip()


def _exec_prompt(model: str, user_message: str):
    agent = Agent(
        model=model,
        tools=[query_internet, run_shell_command],
        print_fn=_print_dark,
    )
    result = agent.add_user_message(user_message)
    print(colored(f"{result}", color="yellow"))


def _print_all_instructions():
    _print_instruction("/?", "Show help")
    _print_instruction("/bye", "Quit")
    _print_instruction("/multi", "Start multiline mode")
    _print_instruction("/end", "Stop multiline mode")
    _print_instruction("/llm", "Get current LLM provider")
    _print_instruction("/llm <llm-provider>", "Set LLM provider (e.g., ollama/mistral:7b-instruct gpt-4o, bedrock/anthropic.claude-3-sonnet-20240229-v1:0)")  # noqa


def _print_instruction(instruction: str, description: str):
    padded_instruction = instruction.ljust(25)
    print(
        "\t".join(
            [
                colored(f" {padded_instruction}", color="yellow", attrs=["dark"]),
                colored(description, attrs=["dark"]),
            ]
        )
    )


def _print_dark(text: str):
    print(colored(f"{text}", attrs=["dark"]))
