import os
import sys
from collections.abc import Callable, Mapping
from typing import Any, Union

from zrb.helper.accessories.color import colored
from zrb.helper.typecheck import typechecked
from zrb.helper.util import to_snake_case

from ..agent import Agent
from ..config import (
    CONVERSATION_LOG_PATH,
    CONVERSATION_VECTOR_LOG_PATH,
    LLM_MODEL,
    RAG_CHUNK_SIZE,
    RAG_EMBEDDING_MODEL,
    RAG_MAX_RESULT_COUNT,
    RAG_OVERLAP,
    SHOULD_SHOW_SYSTEM_PROMPT
)
from ..tools import create_get_changes, create_rag_from_directory

if not os.path.isdir(CONVERSATION_LOG_PATH):
    os.makedirs(CONVERSATION_LOG_PATH)
conversation_rag = create_rag_from_directory(
    tool_name="search_previous_conversation",
    tool_description="Look for any information that probably was in previous conversation between assistant and human",  # noqa
    document_dir_path=CONVERSATION_LOG_PATH,
    vector_db_path=CONVERSATION_VECTOR_LOG_PATH,
)


@typechecked
class Conversation:
    def __init__(
        self,
        model: str = LLM_MODEL,
        should_show_system_prompt: bool = SHOULD_SHOW_SYSTEM_PROMPT,
        enabled_tool_names: list[str] = [],
        available_tools: Mapping[str, Callable[[], Any]] = {},
        initial_user_input: str = "",
    ):
        self._model = model
        self._should_show_system_prompt = should_show_system_prompt
        self._initial_user_input = initial_user_input
        self._previous_messages = []
        self._is_multiline_mode = False
        self._mutiline_user_inputs = []
        self._enabled_tool_names = enabled_tool_names
        self._available_tools = available_tools
        self._available_tools[conversation_rag.__name__] = conversation_rag

    async def loop(self):
        self._print_all_instructions()
        while True:
            try:
                user_input = self._read_user_message()
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
            tools=[
                tool
                for tool_name, tool in self._available_tools.items()
                if tool_name in self._enabled_tool_names
            ],
            conversation_log_path=CONVERSATION_LOG_PATH,
            should_show_system_prompt=self._should_show_system_prompt,
            previous_messages=self._previous_messages,
            print_fn=self._print_dark_indented,
        )
        self._should_show_system_prompt = False
        result = await agent.add_user_message(user_prompt)
        print(colored(f"{result}", color="yellow"))
        self._previous_messages = agent.get_previous_messages()

    def _read_user_message(self) -> str:
        if self._initial_user_input != "":
            line = self._initial_user_input
            self._initial_user_input = ""
            return line
        if not self._is_multiline_mode:
            print(
                colored(">> ", color="green", attrs=["bold"]),
                file=sys.stderr,
                flush=True,
                end="",
            )
        return self._read_input()

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
        if (
            self._process_help_command(line)
            or self._process_model_command(line)
            or self._process_tool_command(line)
        ):
            return
        if line.startswith("/"):
            self._print_red_indented(f"Unknown command {line}")
            self._print_all_instructions()
            return
        return line

    def _process_help_command(self, line: str) -> bool:
        if line.lower() in ["/?", "/help"]:
            self._print_all_instructions()
            return True
        return False

    def _process_tool_command(self, line: str) -> bool:
        if line.lower() == "/clear":
            self._previous_messages = []
            self._print_dark_indented("Context cleared")
            return True
        if line.lower() == "/tool":
            self._print_tool_names()
            return True
        if line.lower().startswith("/tool add"):
            tool_names = self._get_subcommand("/tool add", line).split(" ")
            for tool_name in tool_names:
                if tool_name == "rag":
                    self._add_rag_tool()
                elif tool_name == "git_diff":
                    self._add_git_diff_tool()
                else:
                    self._add_tool(tool_name)
            self._print_tool_names()
            return True
        if line.lower().startswith("/tool rm"):
            tool_names = self._get_subcommand("/tool rm", line).split(" ")
            for tool_name in tool_names:
                self._remove_tool(tool_name)
            self._print_tool_names()
            return True
        return False

    def _add_rag_tool(self):
        document_directory = self._read_param("RAG Document directory", "./document")
        snake_document_directory = to_snake_case(document_directory)
        tool_name = self._read_param(
            "RAG Tool Name", f"retrieve_from_{snake_document_directory}"
        )
        tool_description = self._read_param(
            "RAG Tool Description", f"Retrieve info from {document_directory}"
        )
        model = self._read_param("RAG Embedding Model", RAG_EMBEDDING_MODEL)
        vector_db_path = self._read_param(
            "RAG Vector DB Path", f"{document_directory}-vector"
        )
        vector_db_collection = self._read_param("RAG Vector DB Collection", "documents")
        chunk_size = int(self._read_param("RAG Chunk Size", RAG_CHUNK_SIZE))
        overlap = int(self._read_param("RAG Overlap", RAG_OVERLAP))
        max_result_count = int(
            self._read_param("RAG Max Result Count", RAG_MAX_RESULT_COUNT)
        )
        self._enabled_tool_names.append(tool_name)
        self._available_tools[tool_name] = create_rag_from_directory(
            tool_name=tool_name,
            tool_description=tool_description,
            document_dir_path=document_directory,
            model=model,
            vector_db_path=vector_db_path,
            vector_db_collection=vector_db_collection,
            chunk_size=chunk_size,
            overlap=overlap,
            max_result_count=max_result_count,
        )

    def _add_git_diff_tool(self):
        repo_directory = self._read_param("Git Diff Repo Directory", "./repo")
        snake_repo_directory = to_snake_case(repo_directory)
        tool_name = self._read_param(
            "Git Diff Tool Name", f"get_changes_on_{snake_repo_directory}"
        )
        tool_description = self._read_param(
            "Git Diff Tool Description", f"Retrieve changes on {repo_directory}"
        )
        initial_branch = self._read_param("Git Diff Initial Branch", "main")
        new_branch = self._read_param("Git Diff New Branch", "HEAD")
        self._enabled_tool_names.append(tool_name)
        self._available_tools[tool_name] = create_get_changes(
            tool_name=tool_name,
            tool_description=tool_description,
            directory=repo_directory,
            initial_branch=initial_branch,
            new_branch=new_branch,
        )

    def _process_model_command(self, line: str) -> bool:
        if line.lower().startswith("/model"):
            arg = self._get_subcommand("/model", line)
            if arg != "":
                self._model = arg
            self._print_green_indented(f"Model: {self._model}")
            return True
        return False

    def _read_param(self, caption: str, default_value: str) -> str:
        print(
            " ".join(
                [
                    colored(caption, color="green"),
                    colored(f"[{default_value}]: ", attrs=["dark"]),
                ]
            ),
            file=sys.stderr,
            end="",
            flush=True,
        )
        new_value = self._read_input()
        if new_value != "":
            return new_value
        return f"{default_value}"

    def _read_input(self) -> str:
        return sys.stdin.readline().strip()

    def _get_subcommand(self, command: str, line: str) -> str:
        lower_line = line.lower().lower()
        lower_command = command.lower()
        if len(lower_line) > len(lower_command) and lower_line.startswith(
            lower_command
        ):  # noqa
            return line[len(lower_command) :].strip()
        return ""

    def _add_tool(self, tool_name):
        if tool_name not in self._available_tools:
            self._print_red_indented(f"Tool is not available: {tool_name}")
            return
        if tool_name in self._enabled_tool_names:
            self._print_red_indented(f"Tool is already active: {tool_name}")
            return
        self._enabled_tool_names.append(tool_name)

    def _remove_tool(self, tool_name):
        if tool_name not in self._available_tools:
            self._print_red_indented(f"Tool is not available: {tool_name}")
            return
        if tool_name not in self._enabled_tool_names:
            self._print_red_indented(f"Tool is not active: {tool_name}")
            return
        self._enabled_tool_names.remove(tool_name)

    def _print_tool_names(self):
        self._print_green_indented("Tools:")
        for tool_name in self._available_tools:
            status = "[x]" if tool_name in self._enabled_tool_names else "[ ]"
            self._print_green_indented(f"- {status} {tool_name}")
        self._print_green_indented("- rag (Create new RAG tool)")
        self._print_green_indented("- git_diff (Create new Git Diff tool)")

    def _print_all_instructions(self):
        self._print_instruction("/?", "Show help")
        self._print_instruction("/bye", "Quit")
        self._print_instruction("/clear", "Clear context")
        self._print_instruction("/multi", "Start multiline mode")
        self._print_instruction("/end", "Stop multiline mode")
        self._print_instruction(
            "/model [model]",
            "Get/set current model (e.g., ollama/mistral:7b-instruct, gpt-4o)",
        )  # noqa
        print(file=sys.stderr)
        self._print_instruction("/tool", "Get list of tools")
        self._print_instruction("/tool add <tool-name>", "Add tool")
        self._print_instruction("/tool rm <tool-name>", "Remove tool")

    def _print_instruction(self, instruction: str, description: str):
        padded_instruction = instruction.ljust(22)
        print(
            " ".join(
                [
                    colored(f"    {padded_instruction}", color="yellow"),
                    colored(description, attrs=["dark"]),
                ]
            ),
            file=sys.stderr,
        )

    def _print_dark_indented(self, text: str):
        self._print_dark("\n".join([f"  {line}" for line in text.split("\n")]))

    def _print_red_indented(self, text: str):
        self._print_red("\n".join([f"  {line}" for line in text.split("\n")]))

    def _print_green_indented(self, text: str):
        self._print_green("\n".join([f"  {line}" for line in text.split("\n")]))

    def _print_green(self, text: str):
        print(colored(f"{text}", color="green", attrs=["bold"]), file=sys.stderr)

    def _print_red(self, text: str):
        print(colored(f"{text}", color="red", attrs=["bold"]), file=sys.stderr)

    def _print_dark(self, text: str):
        print(colored(f"{text}", attrs=["dark"]), file=sys.stderr)
