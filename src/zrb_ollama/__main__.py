import asyncio
import os
import sys

from typing import Union, List, Callable
from zrb.helper.accessories.color import colored
from .agent import Agent
from .tools import (
    run_shell_command, query_internet, get_current_location, get_current_weather
)

_AVAILABLE_TOOL_NAMES = [
    "query_internet",
    "run_shell_command",
    "get_current_location",
    "get_current_weather"
]


def prompt():
    model = os.getenv("LLM_MODEL", "ollama/mistral:7b-instruct")
    initial_user_input = "" if len(sys.argv) <= 1 else " ".join(sys.argv[1:])
    conversation = Conversation(
        model=model,
        initial_user_input=initial_user_input
    )
    asyncio.run(conversation.loop())


class Conversation():
    def __init__(
        self,
        model: str,
        initial_user_input: str = ""
    ):
        self._model = model
        self._previous_messages = []
        self._initial_user_input = initial_user_input
        self._is_multiline_mode = False
        self._mutiline_user_inputs = []
        self._tool_names = ['query_internet', 'run_shell_command']

    async def loop(self):
        self._print_all_instructions()
        while True:
            try:
                user_input = self._read_input()
                if user_input.lower() in ["/bye", "/quit", "/q", "/exit"]:
                    self._print_dark("Bye")
                    return
                user_prompt = self._process_input(user_input)
                await self._handle_user_prompt(user_prompt)
            except KeyboardInterrupt:
                self._print_dark("Bye")
                return

    async def _handle_user_prompt(self, user_prompt: str):
        if user_prompt is None or user_prompt == "":
            return
        agent = Agent(
            model=self._model,
            tools=self._get_agent_tools(),
            previous_messages=self._previous_messages,
            print_fn=self._print_dark_indented,
        )
        result = await agent.add_user_message(user_prompt)
        print(colored(f"{result}", color="yellow"))
        self._previous_messages = agent.get_history()

    def _get_agent_tools(self) -> List[Callable]:
        tools = []
        if "query_internet" in self._tool_names:
            tools.append(query_internet)
        if "run_shell_command" in self._tool_names:
            tools.append(run_shell_command)
        if "get_current_location" in self._tool_names:
            tools.append(get_current_location)
        if "get_current_weather" in self._tool_names:
            tools.append(get_current_weather)
        return tools

    def _read_input(self) -> str:
        if self._initial_user_input != "":
            line = self._initial_user_input
            self._initial_user_input = ""
            return line
        if not self._is_multiline_mode:
            self._print_dark("Enter your input:")
        return sys.stdin.readline().strip()

    def _process_input(self, line: str) -> Union[str, None]:
        if self._is_multiline_mode:
            if line.lower() == "/end":
                self._is_multiline_mode = False
                return "\n".join(self._mutiline_user_inputs)
            self._mutiline_user_inputs.append(line)
            return
        if line.lower() in ["/multi", "/multiline"]:
            self._is_multiline_mode = True
            self._mutiline_user_inputs = []
            return
        if line.lower() in ["/?", "/help"]:
            self._print_all_instructions()
            return
        if line.lower() == "/model":
            self._print_dark_indented(f"Model: {self._model}")
            return
        if line.lower().startswith("/model"):
            self._model = line[len("/model"):].strip()
            return
        if line.lower() == "/tool all":
            self._print_available_tool_names()
            return
        if line.lower() == "/tool ls":
            self._print_active_tool_names()
            return
        if line.lower().startswith("/tool add"):
            tool_name = line[len("/tool add"):].strip()
            self._add_tool_name(tool_name)
            return
        if line.lower().startswith("/tool rm"):
            tool_name = line[len("/tool rm"):].strip()
            self._remove_tool_name(tool_name)
            return
        return line

    def _add_tool_name(self, tool_name):
        if tool_name not in _AVAILABLE_TOOL_NAMES:
            self._print_red_indented(f"Tool is not available: {tool_name}")
            return
        if tool_name in self._tool_names:
            self._print_red_indented(f"Tool is already active: {tool_name}")
            return
        self._tool_names.append(tool_name)
        self._print_active_tool_names()

    def _remove_tool_name(self, tool_name):
        if tool_name not in _AVAILABLE_TOOL_NAMES:
            self._print_red_indented(f"Tool is not available: {tool_name}")
            return
        if tool_name not in self._tool_names:
            self._print_red_indented(f"Tool is not active: {tool_name}")
            return
        self._tool_names.remove(tool_name)
        self._print_active_tool_names()

    def _print_active_tool_names(self):
        self._print_dark_indented("Active Tools:")
        for active_tool_name in self._tool_names:
            self._print_dark_indented(f"- {active_tool_name}")

    def _print_available_tool_names(self):
        self._print_dark_indented("Available Tools:")
        for available_tool_name in _AVAILABLE_TOOL_NAMES:
            self._print_dark_indented(f"- {available_tool_name}")

    def _print_all_instructions(self):
        self._print_instruction("/?", "Show help")
        self._print_instruction("/bye", "Quit")
        self._print_instruction("/multi", "Start multiline mode")
        self._print_instruction("/end", "Stop multiline mode")
        self._print_instruction("/model", "Get current model")
        self._print_instruction("/model <model>", "Set model (e.g., ollama/mistral:7b-instruct gpt-4o, bedrock/anthropic.claude-3-sonnet-20240229-v1:0)")  # noqa
        self._print_instruction("/tool all", "Get list of available tools")
        self._print_instruction("/tool ls", "Get list of active tools")
        self._print_instruction("/tool add <tool-name>", "activate tool")
        self._print_instruction("/tool rm <tool-name>", "deactivate tool")

    def _print_instruction(self, instruction: str, description: str):
        padded_instruction = instruction.ljust(22)
        print(
            " ".join([
                colored(f"    {padded_instruction}", color="yellow", attrs=["dark"]),
                colored(description, attrs=["dark"]),
            ]),
            file=sys.stderr
        )

    def _print_dark_indented(self, text: str):
        self._print_dark("\n".join([f"  {line}" for line in text.split("\n")]))

    def _print_red_indented(self, text: str):
        self._print_red("\n".join([f"  {line}" for line in text.split("\n")]))

    def _print_red(self, text: str):
        print(colored(f"{text}", color="red", attrs=["bold"]), file=sys.stderr)

    def _print_dark(self, text: str):
        print(colored(f"{text}", attrs=["dark"]), file=sys.stderr)
