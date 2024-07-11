import asyncio
import os
import sys

from typing import Any, List
from zrb.helper.accessories.color import colored
from .agent import Agent
from .tools import run_shell_command, query_internet


def prompt():
    asyncio.run(async_prompt())


async def async_prompt():
    model = os.getenv("EXAMPLE_MODEL", "ollama/mistral:7b-instruct")
    previous_messages = []
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        previous_messages = await _exec_prompt(model, user_input, previous_messages)
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
                previous_messages = await _exec_prompt(
                    model, user_input, previous_messages
                )
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
        previous_messages = await _exec_prompt(model, user_input, previous_messages)


def _get_line(show_input_prompt: bool) -> str:
    if show_input_prompt:
        _print_dark("Enter your input:")
    return sys.stdin.readline().strip()


async def _exec_prompt(model: str, user_message: str, previous_messages: List[Any]):
    agent = Agent(
        model=model,
        tools=[query_internet, run_shell_command],
        previous_messages=previous_messages,
        print_fn=_print_dark,
    )
    result = await agent.add_user_message(user_message)
    print(colored(f"{result}", color="yellow"))
    return agent.get_history()


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
