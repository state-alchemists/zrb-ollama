import os
import sys
from functools import lru_cache

from langchain.agents import Agent, AgentExecutor, create_react_agent
from langchain.callbacks.manager import CallbackManager
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import BasePromptTemplate
from langchain_core.tools import BaseTool
from zrb import (
    AnyInput,
    AnyTask,
    Env,
    EnvFile,
    Group,
    OnFailed,
    OnReady,
    OnRetry,
    OnSkipped,
    OnStarted,
    OnTriggered,
    OnWaiting,
    Task,
)
from zrb.helper.typecheck import typechecked
from zrb.helper.typing import Any, Callable, Iterable, List, Union

from ..config import (
    CHAT_HISTORY_FILE_NAME,
    CHAT_HISTORY_RETENTION,
    LLM_PROVIDER,
    SYSTEM_PROMPT,
)
from ..factory.llm.default import default_llm_factory
from ..factory.prompt.default import default_prompt_factory
from ..factory.schema import (
    CallbackHandlerFactory,
    LLMFactory,
    PromptFactory,
    ToolFactory,
)
from ..factory.tool.default import default_tool_factories
from .any_prompt_task import AnyPromptTask

# flake8: noqa E501


@typechecked
class PromptTask(AnyPromptTask, Task):
    """
    A class representing a task that handles prompts, providing an interface for managing
    various aspects of prompt-based interactions and executions.

    Attributes:
        name (str): The name of the task.
        history_file (str | None): Optional file path for storing conversation history.
        callback_handler_factories (Iterable[CallbackHandlerFactory]): Factory for creating CallbackHandler.
        tool_factories (Iterable[ToolFactory]): Factory for creating tools.
        llm_factory (LLMFactory | None): Factory for creating LLM.
        prompt_factory (PromptFactory | None): Factory for creating prompt.
        group (Group | None): The group to which this task belongs.
        description (str): Description of the task.
        inputs (List[AnyInput]): List of inputs for the task.
        envs (Iterable[Env]): Iterable of environment variables for the task.
        env_files (Iterable[EnvFile]): Iterable of environment files for the task.
        icon (str | None): Icon for the task.
        color (str | None): Color associated with the task.
        retry (int): Number of retries for the task.
        retry_interval (float | int): Interval between retries.
        upstreams (Iterable[AnyTask]): Iterable of upstream tasks.
        checkers (Iterable[AnyTask]): Iterable of checker tasks.
        checking_interval (float | int): Interval for checking task status.
        on_triggered (OnTriggered | None): Callback for when the task is triggered.
        on_waiting (OnWaiting | None): Callback for when the task is waiting.
        on_skipped (OnSkipped | None): Callback for when the task is skipped.
        on_started (OnStarted | None): Callback for when the task starts.
        on_ready (OnReady | None): Callback for when the task is ready.
        on_retry (OnRetry | None): Callback for when the task retries.
        on_failed (OnFailed | None): Callback for when the task fails.
        should_execute (bool | str | Callable[..., bool]): Condition for executing the task.
        return_upstream_result (bool): Flag to return the result of upstream tasks.

    This class is designed to handle various aspects of prompt-based tasks, including managing
    chat interactions and settings.
    """

    def __init__(
        self,
        name: str,
        input_prompt: str,
        system_prompt: str = SYSTEM_PROMPT,
        history_file: str = CHAT_HISTORY_FILE_NAME,
        chat_history_retention: int = CHAT_HISTORY_RETENTION,
        callback_handler_factories: Iterable[CallbackHandlerFactory] = [],
        tool_factories: Iterable[ToolFactory] = default_tool_factories(),
        llm_provider: str = LLM_PROVIDER,
        llm_factory: LLMFactory = default_llm_factory(),
        prompt_factory: PromptFactory = default_prompt_factory(),
        stop_sequence: Union[bool, List[str]] = True,
        group: Group | None = None,
        description: str = "",
        inputs: List[AnyInput] = [],
        envs: Iterable[Env] = [],
        env_files: Iterable[EnvFile] = [],
        icon: str | None = None,
        color: str | None = None,
        retry: int = 2,
        retry_interval: float | int = 1,
        upstreams: Iterable[AnyTask] = [],
        checkers: Iterable[AnyTask] = [],
        checking_interval: float | int = 0,
        on_triggered: OnTriggered | None = None,
        on_waiting: OnWaiting | None = None,
        on_skipped: OnSkipped | None = None,
        on_started: OnStarted | None = None,
        on_ready: OnReady | None = None,
        on_retry: OnRetry | None = None,
        on_failed: OnFailed | None = None,
        should_execute: bool | str | Callable[..., bool] = True,
        return_upstream_result: bool = False,
    ):
        super().__init__(
            name=name,
            group=group,
            description=description,
            inputs=inputs,
            envs=envs,
            env_files=env_files,
            icon=icon,
            color=color,
            retry=retry,
            retry_interval=retry_interval,
            upstreams=upstreams,
            checkers=checkers,
            checking_interval=checking_interval,
            on_triggered=on_triggered,
            on_waiting=on_waiting,
            on_skipped=on_skipped,
            on_started=on_started,
            on_ready=on_ready,
            on_retry=on_retry,
            on_failed=on_failed,
            should_execute=should_execute,
            return_upstream_result=return_upstream_result,
        )
        self._history_file = history_file
        self._callback_handler_factories = callback_handler_factories
        self._tool_factories = tool_factories
        self._llm_factory = llm_factory
        self._llm_provider = llm_provider
        self._prompt_factory = prompt_factory
        self._input_prompt = input_prompt
        self._system_prompt = system_prompt
        self._chat_history_retention = chat_history_retention
        self._stop_sequence = stop_sequence

    @lru_cache(maxsize=1)
    def get_history_file_name(self) -> str:
        history_file = self._history_file
        rendered_history_file = os.path.expanduser(self.render_str(history_file))
        self.log_info(f"History file: {rendered_history_file}")
        return rendered_history_file

    def clear_history(self):
        if os.path.isfile(self.get_history_file_name()):
            os.remove(self.get_history_file_name())

    @lru_cache(maxsize=1)
    def get_callback_manager(self) -> CallbackManager:
        callback_handler_factories = self._callback_handler_factories
        if len(callback_handler_factories) == 0:
            from ..factory.callback_handler import default_callback_handler_factory

            callback_handler_factories = [default_callback_handler_factory()]
        return CallbackManager(
            handlers=[factory(self) for factory in callback_handler_factories]
        )

    @lru_cache(maxsize=1)
    def get_llm(self) -> BaseLanguageModel:
        return self._llm_factory(self)

    @lru_cache(maxsize=1)
    def get_prompt(self) -> BasePromptTemplate:
        return self._prompt_factory(self)

    @lru_cache(maxsize=1)
    def get_tools(self) -> List[BaseTool]:
        tool_factories = self._tool_factories
        return [tool_factory(self) for tool_factory in tool_factories]

    @lru_cache(maxsize=1)
    def get_agent(self) -> Agent:
        return create_react_agent(
            llm=self.get_llm(),
            tools=self.get_tools(),
            prompt=self.get_prompt(),
            stop_sequence=self._stop_sequence,
        )

    @lru_cache(maxsize=1)
    def get_agent_executor(self) -> AgentExecutor:
        return AgentExecutor(
            agent=self.get_agent(),
            tools=self.get_tools(),
            handle_parsing_errors=True,
            max_iterations=10,
        )

    async def run(self, *args: Any, **kwargs: Any) -> Any:
        chat_history = self._get_chat_history()
        input_prompt = self.render_str(self._input_prompt)
        agent_executor = self.get_agent_executor()
        self.log_info(f"Input: {input_prompt}")
        self.log_info(f"Chat History: {chat_history}")
        result = agent_executor.invoke(
            {
                "input": input_prompt,
                "chat_history": chat_history,
            }
        )
        ai_output = result["output"]
        print("", file=sys.stderr)
        print("", file=sys.stderr)
        print(ai_output, file=sys.stderr, flush=True)
        self._save_chat_history(input_prompt=input_prompt, ai_output=ai_output)

    def _get_chat_history(self) -> str:
        if os.path.isfile(self.get_history_file_name()):
            with open(self.get_history_file_name(), "r") as history_file:
                all_history = history_file.read()
                lines = all_history.split("\n")
                if len(lines) == 0:
                    return ""
                human_count = 0
                for i in range(len(lines) - 1, -1, -1):
                    if lines[i].startswith("Human:"):
                        human_count += 1
                    if human_count == self._chat_history_retention:
                        return "\n".join(lines[i:])
                return all_history
        return ""

    def _save_chat_history(self, input_prompt: str, ai_output: str):
        with open(self.get_history_file_name(), "a") as history_file:
            history_file.write(f"Human: {input_prompt}\n")
            history_file.write(f"Assistant: {ai_output}\n")
