import asyncio
import os
import sys

from typing import Union, List
from zrb.helper.accessories.color import colored
from zrb.helper.util import to_snake_case
from .agent import Agent
from .tools import (
    run_shell_command,
    query_internet,
    get_current_location,
    get_current_weather,
    create_rag,
    create_get_changes
)


def prompt():
    model = os.getenv("LLM_MODEL", "ollama/mistral:7b-instruct")
    initial_user_input = "" if len(sys.argv) <= 1 else " ".join(sys.argv[1:])
    tool_names = [name.strip() for name in os.getenv("TOOLS", "query_internet, run_shell_command").split(",")]  # noqa
    rag_embedding_model = os.getenv("RAG_EMBEDDING_MODEL", "ollama/nomic-embed-text")
    rag_chunk_size = int(os.getenv("RAG_CHUNK_SIZE", "1024"))
    rag_overlap = int(os.getenv("RAG_OVERLAP", "256"))
    rag_max_result_count = int(os.getenv("RAG_MAX_RESULT_COUNT", "5"))
    conversation = Conversation(
        model=model,
        tool_names=tool_names,
        initial_user_input=initial_user_input,
        default_rag_embedding_model=rag_embedding_model,
        default_rag_chunk_size=rag_chunk_size,
        default_rag_overlap=rag_overlap,
        default_rag_max_result_count=rag_max_result_count,
    )
    asyncio.run(conversation.loop())


class Conversation():
    def __init__(
        self,
        model: str,
        tool_names: List[str],
        initial_user_input: str,
        default_rag_embedding_model: str,
        default_rag_chunk_size: int,
        default_rag_overlap: int,
        default_rag_max_result_count: int,
    ):
        self._model = model
        self._initial_user_input = initial_user_input
        self._default_rag_embedding_model = default_rag_embedding_model
        self._default_rag_chunk_size = default_rag_chunk_size
        self._default_rag_overlap = default_rag_overlap
        self._default_rag_max_result_count = default_rag_max_result_count
        self._previous_messages = []
        self._is_multiline_mode = False
        self._mutiline_user_inputs = []
        self._tool_names = tool_names
        self._available_tools = {
            "query_internet": query_internet,
            "run_shell_command": run_shell_command,
            "get_current_location": get_current_location,
            "get_current_weather": get_current_weather,
        }

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
                if tool_name in self._tool_names
            ],
            previous_messages=self._previous_messages,
            print_fn=self._print_dark_indented,
        )
        result = await agent.add_user_message(user_prompt)
        print(colored(f"{result}", color="yellow"))
        self._previous_messages = agent.get_history()

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
                end=""
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
            self._process_help_command(line) or
            self._process_model_command(line) or
            self._process_tool_command(line)
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
        if line.lower() == "/tool":
            self._print_tool_names()
            return True
        if line.lower() == "/tool all":
            self._print_available_tool_names()
            return True
        if line.lower().startswith("/tool add"):
            tool_name = self._get_subcommand("/tool add", line)
            if tool_name == "rag":
                self._add_rag_tool()
                return True
            if tool_name == "git_diff":
                self._add_git_diff_tool()
                return True
            self._add_tool(tool_name)
            return True
        if line.lower().startswith("/tool rm"):
            tool_name = self._get_subcommand("/tool rm", line)
            self._remove_tool(tool_name)
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
        model = self._read_param(
            "RAG Embedding Model", self._default_rag_embedding_model
        )
        vector_db_path = self._read_param(
            "RAG Vector DB Path", f"{document_directory}-vector"
        )
        vector_db_collection = self._read_param("RAG Vector DB Collection", "documents")
        chunk_size = int(self._read_param(
            "RAG Chunk Size", self._default_rag_chunk_size
        ))
        overlap = int(self._read_param("RAG Overlap", self._default_rag_overlap))
        max_result_count = int(self._read_param(
            "RAG Max Result Count", self._default_rag_max_result_count
        ))
        self._tool_names.append(tool_name)
        self._available_tools[tool_name] = create_rag(
            tool_name=tool_name,
            tool_description=tool_description,
            documents=self._get_rag_documents(document_directory),
            model=model,
            vector_db_path=vector_db_path,
            vector_db_collection=vector_db_collection,
            chunk_size=chunk_size,
            overlap=overlap,
            max_result_count=max_result_count
        )

    def _get_rag_documents(self, directory):
        # Walk through the directory
        documents = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                documents.append(self._get_text_reader(file_path))
        return documents

    def _get_text_reader(self, file_path: str):
        def getter():
            with open(file_path, 'r', encoding="utf-8") as f:
                content = f.read()
            return content
        return getter

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
        self._tool_names.append(tool_name)
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
            " ".join([
                colored(caption, color="green"),
                colored(f"[{default_value}]: ", attrs=["dark"]),
            ]),
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
        if len(lower_line) > len(lower_command) and lower_line.startswith(lower_command):  # noqa
            return line[len(lower_command):].strip()
        return ""

    def _add_tool(self, tool_name):
        if tool_name not in self._available_tools:
            self._print_red_indented(f"Tool is not available: {tool_name}")
            return
        if tool_name in self._tool_names:
            self._print_red_indented(f"Tool is already active: {tool_name}")
            return
        self._tool_names.append(tool_name)
        self._print_tool_names()

    def _remove_tool(self, tool_name):
        if tool_name not in self._available_tools:
            self._print_red_indented(f"Tool is not available: {tool_name}")
            return
        if tool_name not in self._tool_names:
            self._print_red_indented(f"Tool is not active: {tool_name}")
            return
        self._tool_names.remove(tool_name)
        self._print_tool_names()

    def _print_tool_names(self):
        self._print_green_indented("Active Tools:")
        for active_tool_name in self._tool_names:
            self._print_green_indented(f"- {active_tool_name}")

    def _print_available_tool_names(self):
        self._print_green_indented("Available Tools:")
        for available_tool_name in self._available_tools:
            self._print_green_indented(f"- {available_tool_name}")
        self._print_green_indented("- rag")
        self._print_green_indented("- git_diff")

    def _print_all_instructions(self):
        self._print_instruction("/?", "Show help")
        self._print_instruction("/bye", "Quit")
        self._print_instruction("/multi", "Start multiline mode")
        self._print_instruction("/end", "Stop multiline mode")
        self._print_instruction("/model [model]", "Get/set current model (e.g., ollama/mistral:7b-instruct, gpt-4o)")  # noqa
        print(file=sys.stderr)
        self._print_instruction("/tool", "Get list of tools")
        self._print_instruction("/tool all", "Get list of available tools")
        self._print_instruction("/tool add <tool-name>", "Add tool")
        self._print_instruction("/tool rm <tool-name>", "Remove tool")

    def _print_instruction(self, instruction: str, description: str):
        padded_instruction = instruction.ljust(22)
        print(
            " ".join([
                colored(f"    {padded_instruction}", color="yellow"),
                colored(description, attrs=["dark"]),
            ]),
            file=sys.stderr
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
