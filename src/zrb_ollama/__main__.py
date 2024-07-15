import asyncio
import os
import sys

from typing import Union, List, Callable
from zrb.helper.accessories.color import colored
from .agent import Agent
from .tools import (
    run_shell_command,
    query_internet,
    get_current_location,
    get_current_weather,
    create_rag,
    create_get_changes
)

_AVAILABLE_TOOL_NAMES = [
    "query_internet",
    "run_shell_command",
    "get_current_location",
    "get_current_weather",
    "rag",
    "git_diff",
]


def prompt():
    model = os.getenv("LLM_MODEL", "ollama/mistral:7b-instruct")
    initial_user_input = "" if len(sys.argv) <= 1 else " ".join(sys.argv[1:])
    tool_names = [name.strip() for name in os.getenv("TOOLS", "query_internet, run_shell_command").split(",")]  # noqa
    diff_tool_name = os.getenv("DIFF_TOOL_NAME", "get_diff")
    diff_tool_description = os.getenv(
        "DIFF_TOOL_DESCRIPTION", "Get git diff from repository"
    )
    diff_repo_directory = os.getenv("DIFF_REPO_DIRECTORY", "./repo")
    diff_initial_branch = os.getenv("DIFF_INITIAL_BRANCH", "main")
    diff_new_branch = os.getenv("DIFF_NEW_BRANCH", "HEAD")
    rag_tool_name = os.getenv("RAG_TOOL_NAME", "retrieve")
    rag_tool_description = os.getenv("RAG_TOOL_DESCRIPTION", "Retrieving document")
    rag_document_directory = os.getenv("RAG_DOCUMENT_DIRECTORY", "./document")
    rag_embedding_model = os.getenv("RAG_EMBEDDING_MODEL", "ollama/nomic-embed-text")
    rag_vector_db_path = os.getenv("RAG_VECTOR_DB_PATH", "./chroma")
    rag_vector_db_collection = os.getenv("RAG_VECTOR_DB_COLLECTION", "documents")
    rag_chunk_size = int(os.getenv("RAG_CHUNK_SIZE", "1024"))
    rag_overlap = int(os.getenv("RAG_OVERLAP", "256"))
    rag_max_result_count = int(os.getenv("RAG_MAX_RESULT_COUNT", "5"))
    conversation = Conversation(
        model=model,
        tool_names=tool_names,
        initial_user_input=initial_user_input,
        diff_tool_name=diff_tool_name,
        diff_tool_description=diff_tool_description,
        diff_repo_directory=diff_repo_directory,
        diff_initial_branch=diff_initial_branch,
        diff_new_branch=diff_new_branch,
        rag_tool_name=rag_tool_name,
        rag_tool_description=rag_tool_description,
        rag_document_directory=rag_document_directory,
        rag_embedding_model=rag_embedding_model,
        rag_vector_db_path=rag_vector_db_path,
        rag_vector_db_collection=rag_vector_db_collection,
        rag_chunk_size=rag_chunk_size,
        rag_overlap=rag_overlap,
        rag_max_result_count=rag_max_result_count,
    )
    asyncio.run(conversation.loop())


class Conversation():
    def __init__(
        self,
        model: str,
        tool_names: List[str],
        initial_user_input: str,
        diff_tool_name: str,
        diff_tool_description: str,
        diff_repo_directory: str,
        diff_initial_branch: str,
        diff_new_branch: str,
        rag_tool_name: str,
        rag_tool_description: str,
        rag_document_directory: str,
        rag_embedding_model: str,
        rag_vector_db_path: str,
        rag_vector_db_collection: str,
        rag_chunk_size: int,
        rag_overlap: int,
        rag_max_result_count: int,
    ):
        self._model = model
        self._initial_user_input = initial_user_input
        self._diff_tool_name = diff_tool_name
        self._diff_tool_description = diff_tool_description
        self._diff_repo_directory = diff_repo_directory
        self._diff_initial_branch = diff_initial_branch
        self._diff_new_branch = diff_new_branch
        self._rag_document_directory = rag_document_directory
        self._rag_tool_name = rag_tool_name
        self._rag_tool_description = rag_tool_description
        self._rag_embedding_model = rag_embedding_model
        self._rag_vector_db_path = rag_vector_db_path
        self._rag_vector_db_collection = rag_vector_db_collection
        self._rag_chunk_size = rag_chunk_size
        self._rag_overlap = rag_overlap
        self._rag_max_result_count = rag_max_result_count
        self._previous_messages = []
        self._is_multiline_mode = False
        self._mutiline_user_inputs = []
        self._tool_names = tool_names

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
        if "rag" in self._tool_names:
            if os.path.isdir(self._rag_document_directory):
                tools.append(create_rag(
                    tool_name=self._rag_tool_name,
                    tool_description=self._rag_tool_description,
                    documents=self._get_rag_documents(self._rag_document_directory),
                    model=self._rag_embedding_model,
                    vector_db_path=self._rag_vector_db_path,
                    vector_db_collection=self._rag_vector_db_collection,
                    reset_db=True,
                    chunk_size=self._rag_chunk_size,
                    overlap=self._rag_overlap,
                    max_result_count=self._rag_max_result_count
                ))
            else:
                self._print_red(f"Invalid RAG Document Directory: {self._rag_document_directory}. To set a valid one, please perform `/rag document-directory [directory]`")  # noqa
        if "git_diff" in self._tool_names:
            if os.path.isdir(self._diff_repo_directory):
                tools.append(create_get_changes(
                    tool_name=self._diff_tool_name,
                    tool_description=self._diff_tool_description,
                    initial_branch=self._diff_initial_branch,
                    new_branch=self._diff_new_branch,
                    directory=self._diff_repo_directory
                ))
            else:
                self._print_red(f"Invalid Git Diff Repo Directory: {self._diff_repo_directory}. To set a valid one, please perform `/git-diff repo-directory [directory]`")  # noqa
        return tools

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

    def _read_user_message(self) -> str:
        if self._initial_user_input != "":
            line = self._initial_user_input
            self._initial_user_input = ""
            return line
        if not self._is_multiline_mode:
            self._print_green("\nEnter your input:")
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
        return line

    def _process_help_command(self, line: str) -> bool:
        if line.lower() in ["/?", "/help"]:
            self._print_all_instructions()
            return True
        return False

    def _process_tool_command(self, line: str) -> bool:
        if line.lower() == "/tool":
            self._print_active_tool_names()
            return True
        if line.lower() == "/tool all":
            self._print_available_tool_names()
            return True
        if line.lower().startswith("/tool add"):
            tool_name = self._get_subcommand("/tool add", line)
            if tool_name == "rag":
                self._ask_rag_param()
            if tool_name == "git_diff":
                self._ask_git_diff_param()
            self._activate_tool(tool_name)
            return True
        if line.lower().startswith("/tool rm"):
            tool_name = self._get_subcommand("/tool rm", line)
            self._deactivate_tool(tool_name)
            return True
        return False

    def _ask_rag_param(self):
        self._rag_tool_name = self._read_param(
            "RAG Tool Name", self._rag_tool_name
        )
        self._rag_tool_description = self._read_param(
            "RAG Tool Description", self._rag_tool_description
        )
        self._rag_document_directory = self._read_param(
            "RAG Tool Description", self._rag_document_directory
        )
        self._rag_embedding_model = self._read_param(
            "RAG Embedding Model", self._rag_embedding_model
        )
        self._rag_vector_db_path = self._read_param(
            "RAG Vector DB Path", self._rag_vector_db_path
        )
        self._rag_vector_db_collection = self._read_param(
            "RAG Vector DB Collection", self._rag_vector_db_collection
        )
        self._rag_chunk_size = int(self._read_param(
            "RAG Chunk Size", self._rag_chunk_size
        ))
        self._rag_overlap = int(self._read_param(
            "RAG Overlap", self._rag_overlap
        ))
        self._rag_max_result_count = int(self._read_param(
            "RAG Max Result Count", self._rag_max_result_count
        ))

    def _ask_git_diff_param(self):
        self._diff_tool_name = self._read_param(
            "Git Diff Tool Name", self._diff_tool_name
        )
        self._diff_tool_description = self._read_param(
            "Git Diff Tool Description", self._diff_tool_description
        )
        self._diff_repo_directory = self._read_param(
            "Git Diff Repo Directory", self._diff_repo_directory
        )
        self._diff_initial_branch = self._read_param(
            "Git Diff Initial Branch", self._diff_initial_branch
        )
        self._diff_new_branch = self._read_param(
            "Git Diff New Branch", self._diff_new_branch
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
        self._print_green(f"{caption} [{default_value}]:")
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

    def _activate_tool(self, tool_name):
        if tool_name not in _AVAILABLE_TOOL_NAMES:
            self._print_red_indented(f"Tool is not available: {tool_name}")
            return
        if tool_name in self._tool_names:
            self._print_red_indented(f"Tool is already active: {tool_name}")
            return
        self._tool_names.append(tool_name)
        self._print_active_tool_names()

    def _deactivate_tool(self, tool_name):
        if tool_name not in _AVAILABLE_TOOL_NAMES:
            self._print_red_indented(f"Tool is not available: {tool_name}")
            return
        if tool_name not in self._tool_names:
            self._print_red_indented(f"Tool is not active: {tool_name}")
            return
        self._tool_names.remove(tool_name)
        self._print_active_tool_names()

    def _print_active_tool_names(self):
        self._print_green_indented("Active Tools:")
        for active_tool_name in self._tool_names:
            self._print_green_indented(f"- {active_tool_name}")

    def _print_available_tool_names(self):
        self._print_green_indented("Available Tools:")
        for available_tool_name in _AVAILABLE_TOOL_NAMES:
            self._print_green_indented(f"- {available_tool_name}")

    def _print_all_instructions(self):
        self._print_instruction("/?", "Show help")
        self._print_instruction("/bye", "Quit")
        self._print_instruction("/multi", "Start multiline mode")
        self._print_instruction("/end", "Stop multiline mode")
        self._print_instruction("/model [model]", "Get/set current model (e.g., ollama/mistral:7b-instruct, gpt-4o)")  # noqa
        print(file=sys.stderr)
        self._print_instruction("/tool", "Get list of active tools")
        self._print_instruction("/tool all", "Get list of available tools")
        self._print_instruction("/tool add <tool-name>", "activate tool")
        self._print_instruction("/tool rm <tool-name>", "deactivate tool")

    def _print_instruction(self, instruction: str, description: str):
        padded_instruction = instruction.ljust(40)
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
