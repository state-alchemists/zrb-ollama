from functools import lru_cache
from langchain.callbacks.manager import CallbackManager
from langchain.chains import LLMChain
from langchain.memory.chat_memory import BaseChatMemory
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.agents import Agent, AgentExecutor, Tool
from zrb.helper.typecheck import typechecked
from zrb.helper.typing import Any, Callable, Iterable, List, Mapping
from zrb import (
    AnyTask, Task, Env, EnvFile, Group, AnyInput,
    OnFailed, OnReady, OnRetry, OnSkipped, OnStarted, OnTriggered, OnWaiting
)
from ..factory.schema import (
    LLMChainFactory, CallbackManagerFactory, ChatModelFactory,
    ChatPromptTemplateFactory, ChatMemoryFactory, AgentExecutorFactory,
    AgentFactory, PromptTemplateFactory, AgentToolFactory
)
from .any_prompt_task import AnyPromptTask
from ..config import OPENAI_API_KEY

import json
import os
import sys

# flake8: noqa E501

@typechecked
class PromptTask(AnyPromptTask, Task):
    """
    A class representing a task that handles prompts, providing an interface for managing
    various aspects of prompt-based interactions and executions.

    Attributes:
        name (str): The name of the task.
        prompt (str): The user prompt for the task.
        system_prompt (str): An optional system prompt for the task.
        history_file (str | None): Optional file path for storing conversation history.
        is_agent (str | bool): Flag to determine if the task acts as an agent.
        llm_chain_factory (LLMChainFactory | None): Factory for creating LLM chains.
        callback_manager_factory (CallbackManagerFactory | None): Factory for creating callback managers.
        chat_model_factory (ChatModelFactory | None): Factory for creating chat models.
        chat_prompt_template_factory (ChatPromptTemplateFactory | None): Factory for creating chat prompt templates.
        chat_memory_factory (ChatMemoryFactory | None): Factory for creating chat memory.
        agent_executor_factory (AgentExecutorFactory | None): Factory for creating agent executors.
        agent_factory (AgentFactory | None): Factory for creating agents.
        agent_llm_chain_factory (LLMChainFactory | None): Factory for creating agent LLM chains.
        agent_prompt_template_factory (PromptTemplateFactory | None): Factory for creating agent prompt templates.
        agent_tool_factories (List[AgentToolFactory]): List of factories for creating agent tools.
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
    chat interactions, executing agents or LLM chains, and handling task-related callbacks and settings.
    """
    def __init__(
        self,
        name: str,
        prompt: str,
        system_prompt: str = '',
        history_file: str | None = None,
        is_agent: str | bool = False,
        llm_chain_factory: LLMChainFactory | None = None,
        callback_manager_factory: CallbackManagerFactory | None = None,
        chat_model_factory: ChatModelFactory | None = None,
        chat_prompt_template_factory: ChatPromptTemplateFactory | None = None,
        chat_memory_factory: ChatMemoryFactory | None = None,
        agent_executor_factory: AgentExecutorFactory | None = None,
        agent_factory: AgentFactory | None = None,
        agent_llm_chain_factory: LLMChainFactory | None = None,
        agent_prompt_template_factory: PromptTemplateFactory | None = None,
        agent_tool_factories: List[AgentToolFactory] = [],
        group: Group | None = None,
        description: str = '',
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
        return_upstream_result: bool = False
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
            return_upstream_result=return_upstream_result
        )
        self._is_agent = is_agent
        self._user_prompt = prompt
        self._system_prompt = system_prompt
        self._history_file_name = history_file
        self._llm_chain_factory = llm_chain_factory
        self._create_callback_manager = callback_manager_factory
        self._create_chat_model = chat_model_factory
        self._create_chat_prompt_template = chat_prompt_template_factory
        self._create_chat_memory = chat_memory_factory
        self._agent_executor_factory = agent_executor_factory
        self._agent_factory = agent_factory
        self._agent_llm_chain_factory = agent_llm_chain_factory
        self._agent_prompt_template_factory = agent_prompt_template_factory
        self._agent_tool_factories = agent_tool_factories

    async def run(self, *args: Any, **kwargs: Any) -> Any:
        if self.render_bool(self._is_agent):
            return await self.run_agent_executor(*args, **kwargs)
        return await self.run_llm_chain(*args, **kwargs)

    async def run_llm_chain(self, *args: Any, **kwargs: Any) -> Any:
        llm_chain = self.get_llm_chain()
        user_prompt = self.get_rendered_user_prompt()
        llm_response = llm_chain.run(question=user_prompt)
        self.save_chat_context(input=user_prompt, output=llm_response)
        print('', file=sys.stderr, flush=True)
        return llm_response

    async def run_agent_executor(self, *args: Any, **kwargs: Any) -> Any:
        agent = self.get_agent_executor()
        user_prompt = self.get_rendered_user_prompt()
        agent_response = agent.run(question=user_prompt)
        self.save_chat_context(input=user_prompt, output=agent_response)
        print('', file=sys.stderr, flush=True)
        return agent_response

    @lru_cache(maxsize=1)
    def get_callback_manager(self) -> CallbackManager:
        if self._create_callback_manager is not None:
            return self._create_callback_manager(self)
        from ..factory.callback_manager import callback_manager_factory
        create_callback_manager = callback_manager_factory()
        return create_callback_manager(self)

    @lru_cache(maxsize=1)
    def get_chat_memory(self) -> BaseChatMemory:
        if self._create_chat_memory is not None:
            chat_memory = self._create_chat_memory(self)
            return self.load_chat_context_to_memory(chat_memory)
        from ..factory.chat_memory import chat_conversation_buffer_memory_factory  # noqa
        create_chat_memory = chat_conversation_buffer_memory_factory()
        chat_memory = create_chat_memory(self)
        return self.load_chat_context_to_memory(chat_memory)

    @lru_cache(maxsize=1)
    def get_chat_model(self) -> BaseChatModel:
        if self._create_chat_model is not None:
            return self._create_chat_model(self)
        from ..factory.chat_model import (
            ollama_chat_model_factory, openai_chat_model_factory
        )
        if OPENAI_API_KEY != '':
            create_chat_model = openai_chat_model_factory()
            return create_chat_model(self)
        create_chat_model = ollama_chat_model_factory()
        return create_chat_model(self)

    @lru_cache(maxsize=1)
    def get_chat_prompt_template(self) -> ChatPromptTemplate:
        if self._create_chat_prompt_template is not None:
            return self._create_chat_prompt_template(self)
        from ..factory.chat_prompt_template import chat_prompt_template_factory
        create_chat_prompt_template = chat_prompt_template_factory()
        return create_chat_prompt_template(self)

    @lru_cache(maxsize=1)
    def get_llm_chain(self) -> LLMChain:
        if self._llm_chain_factory is not None:
            return self._llm_chain_factory(self)
        from ..factory.llm_chain import llm_chain_factory
        create_llm_chain = llm_chain_factory(verbose=False)
        return create_llm_chain(self)

    @lru_cache(maxsize=1)
    def get_agent_executor(self) -> AgentExecutor | None:
        if self._agent_executor_factory is not None:
            return self._agent_executor_factory(self)
        from ..factory.agent_executor import agent_executor_factory
        create_agent_executor = agent_executor_factory()
        return create_agent_executor(self)

    @lru_cache(maxsize=1)
    def get_agent(self) -> Agent:
        if self._agent_factory is not None:
            return self._agent_factory(self)
        from ..factory.agent import agent_factory
        create_agent = agent_factory()
        return create_agent(self)

    @lru_cache(maxsize=1)
    def get_agent_llm_chain(self) -> LLMChain:
        if self._agent_llm_chain_factory is not None:
            return self._agent_llm_chain_factory(self)
        from ..factory.agent_llm_chain import agent_llm_chain_factory
        create_agent_llm_chain = agent_llm_chain_factory(verbose=False)
        return create_agent_llm_chain(self)

    @lru_cache(maxsize=1)
    def get_agent_prompt_template(self) -> PromptTemplate:
        if self._agent_prompt_template_factory is not None:
            return self._agent_prompt_template_factory(self)
        from ..factory.agent_prompt_template import agent_prompt_template_factory  # noqa
        create_agent_prompt_template = agent_prompt_template_factory()
        return create_agent_prompt_template(self)

    @lru_cache(maxsize=1)
    def get_agent_tools(self) -> List[Tool]:
        if len(self._agent_tool_factories) > 0:
            return [
                tool_factory(self)
                for tool_factory in self._agent_tool_factories
            ]
        from ..factory.agent_tool import duckduckgo_search_agent_tool_factory
        create_duckduckgo_search = duckduckgo_search_agent_tool_factory()
        return [create_duckduckgo_search(self)]

    def load_chat_context_to_memory(
        self, memory: BaseChatMemory
    ) -> BaseChatMemory:
        conversations = self.get_chat_context()
        if conversations is None:
            return memory
        for conversation in conversations:
            chat_input = conversation.get('input')
            chat_output = conversation.get('output')
            memory.save_context(
                {'input': chat_input}, {'output': chat_output}
            )
        return memory

    @lru_cache(maxsize=1)
    def save_chat_context(self, input: Any, output: Any):
        history_file_name = self.get_rendered_history_file_name()
        if history_file_name is None:
            return
        conversations = self.get_chat_context()
        if conversations is None:
            conversations: List[Mapping[str, Mapping[str, Any]]] = []
        conversations.append({
            'input': input,
            'output': output
        })
        with open(history_file_name, 'w') as file:
            file.write(json.dumps(conversations))

    @lru_cache(maxsize=1)
    def get_chat_context(self) -> List[Mapping[str, Mapping[str, Any]]] | None:
        history_file_name = self.get_rendered_history_file_name()
        if history_file_name is None or not os.path.isfile(history_file_name):
            return None
        with open(history_file_name, 'r') as file:
            return json.loads(file.read())

    @lru_cache(maxsize=1)
    def get_rendered_history_file_name(self) -> str | None:
        if self._history_file_name is None:
            return None
        return os.path.expanduser(self.render_str(self._history_file_name))

    @lru_cache(maxsize=1)
    def get_rendered_user_prompt(self) -> Any:
        return self.render_str(self._user_prompt)

    @lru_cache(maxsize=1)
    def get_rendered_system_prompt(self) -> str:
        return self.render_str(self._system_prompt)
