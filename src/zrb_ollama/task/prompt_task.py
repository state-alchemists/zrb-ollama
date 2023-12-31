from functools import lru_cache
from langchain.callbacks.manager import CallbackManager
from langchain.chains import LLMChain
from langchain.memory.chat_memory import BaseChatMemory
from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from zrb.helper.typecheck import typechecked
from zrb.helper.typing import Any, Callable, Iterable, List, Mapping
from zrb import (
    AnyTask, Task, Env, EnvFile, Group, AnyInput,
    OnFailed, OnReady, OnRetry, OnSkipped, OnStarted, OnTriggered, OnWaiting
)
from ..factory.schema import (
    LLMChainFactory, CallbackManagerFactory, ChatModelFactory,
    ChatPromptTemplateFactory, ChatMemoryFactory
)
from ..factory.callback_manager import callback_manager_factory as make_callback_manager_factory  # noqa
from ..factory.chat_memory import chat_conversation_buffer_memory_factory as make_chat_memory_factory  # noqa
from ..factory.chat_model import ollama_chat_model_factory as make_chat_model_factory  # noqa
from ..factory.chat_prompt_template import chat_prompt_template_factory as make_chat_prompt_template_factory  # noqa
from ..factory.llm_chain import llm_chain_factory as make_llm_chain_factory
from .any_prompt_task import AnyPromptTask

import json
import os
import sys


@typechecked
class PromptTask(AnyPromptTask, Task):
    def __init__(
        self,
        name: str,
        prompt: str,
        system_prompt: str = '',
        history_file: str | None = None,
        llm_chain_factory: LLMChainFactory | None = None,
        callback_manager_factory: CallbackManagerFactory | None = None,
        chat_model_factory: ChatModelFactory | None = None,
        chat_prompt_template_factory: ChatPromptTemplateFactory | None = None,
        chat_memory_factory: ChatMemoryFactory | None = None,
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
        self._user_prompt = prompt
        self._system_prompt = system_prompt
        self._history_file_name = history_file
        self._llm_chain_factory = llm_chain_factory
        self._create_callback_manager = callback_manager_factory
        self._create_chat_model = chat_model_factory
        self._create_chat_prompt_template = chat_prompt_template_factory
        self._create_chat_memory = chat_memory_factory

    async def run(self, *args: Any, **kwargs: Any) -> Any:
        chain = self.get_llm_chain()
        user_prompt = self.get_rendered_user_prompt()
        llm_response = chain.run(user_prompt)
        self.save_chat_context(input=user_prompt, output=llm_response)
        print('', file=sys.stderr, flush=True)
        return llm_response

    @lru_cache(maxsize=1)
    def get_callback_manager(self) -> CallbackManager:
        if self._create_callback_manager is not None:
            return self._create_callback_manager(self)
        create_callback_manager = make_callback_manager_factory()
        return create_callback_manager(self)

    @lru_cache(maxsize=1)
    def get_chat_memory(self) -> BaseChatMemory:
        if self._create_chat_memory is not None:
            chat_memory = self._create_chat_memory(self)
            return self.load_chat_context_to_memory(chat_memory)
        create_chat_memory = make_chat_memory_factory()
        chat_memory = create_chat_memory(self)
        return self.load_chat_context_to_memory(chat_memory)

    @lru_cache(maxsize=1)
    def get_chat_model(self) -> BaseChatModel:
        if self._create_chat_model is not None:
            return self._create_chat_model(self)
        create_chat_model = make_chat_model_factory()
        return create_chat_model(self)

    @lru_cache(maxsize=1)
    def get_chat_prompt_template(self) -> ChatPromptTemplate:
        if self._create_chat_prompt_template is not None:
            return self._create_chat_prompt_template(self)
        create_chat_prompt_template = make_chat_prompt_template_factory()
        return create_chat_prompt_template(self)

    @lru_cache(maxsize=1)
    def get_llm_chain(self) -> LLMChain:
        if self._llm_chain_factory is not None:
            return self._llm_chain_factory(self)
        create_llm_chain = make_llm_chain_factory(verbose=False)
        return create_llm_chain(self)

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
