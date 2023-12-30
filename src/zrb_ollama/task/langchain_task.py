from zrb import Task
from zrb.helper.typecheck import typechecked
from zrb.helper.typing import Any, Callable, Iterable, List
from zrb.helper.accessories.color import colored
from zrb.task.any_task import AnyTask
from zrb.task.any_task_event_handler import (
    OnFailed, OnReady, OnRetry, OnSkipped, OnStarted, OnTriggered, OnWaiting
)
from zrb.task_env.env import Env
from zrb.task_env.env_file import EnvFile
from zrb.task_group.group import Group
from zrb.task_input.any_input import AnyInput
from ..config import DEFAULT_MODEL
from langchain_core.messages import BaseMessage
from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import (
    StreamingStdOutCallbackHandler
)
from langchain.prompts import PromptTemplate
from langchain.memory import FileChatMessageHistory, ConversationBufferMemory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables import Runnable
from langchain_core.language_models import LanguageModelInput


import os
import sys

LLM = Runnable[LanguageModelInput, str] | Runnable[LanguageModelInput, BaseMessage]  # noqa


class LLMCallbackHandler(StreamingStdOutCallbackHandler):

    def __init__(self) -> None:
        super().__init__()
        self._is_first_token = False

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        shown_text = '\n    '.join(token.split('\n'))
        if self._is_first_token:
            shown_text = ''.join(['    ', shown_text])
        print(
            colored(shown_text, attrs=['dark']),
            file=sys.stderr, end='', flush=True
        )
        self._is_first_token = False


@typechecked
class LLMTask(Task):

    def __init__(
        self,
        name: str,
        prompt: str,
        history_file: str | None = None,
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
        self._history_file = history_file
        self._llm_chain: LLMChain | None = None
        self._is_llm_chain_created: bool = False
        self._llm_prompt_template: PromptTemplate | None = None
        self._is_llm_prompt_template_created: bool = False
        self._llm_callback_manager: CallbackManager | None = None
        self._is_llm_callback_manager_created: bool = False
        self._llm_conversation_buffer_memory: ConversationBufferMemory | None = None  # noqa
        self._is_llm_conversation_buffer_memory_created: bool = False
        self._llm: LLM | None = None
        self._is_llm_created = None
        self._parsed_user_prompt: str | None = None

    async def run(self, *args: Any, **kwargs: Any) -> Any:
        chain = self.get_llm_chain()
        result = chain.run(self.get_user_prompt())
        print(chain.memory.json())
        return result

    def create_llm_chain(self) -> LLMChain:
        return LLMChain(
            llm=self.get_llm(),
            prompt=self.get_llm_prompt_template(),
            memory=self.get_llm_conversation_buffer_memory(),
            verbose=False
        )

    def get_llm_chain(self) -> LLMChain:
        if not self._is_llm_chain_created:
            self._llm_chain = self.create_llm_chain()
            self._is_llm_chain_created = True
        return self._llm_chain

    def create_llm(self) -> LLM:
        return Ollama(
            model=DEFAULT_MODEL,
            callback_manager=self.get_llm_callback_manager(),
        )

    def get_llm(self) -> LLM:
        if not self._is_llm_created:
            self._llm = self.create_llm()
            self._is_llm_created = True
        return self._llm

    def create_llm_callback_manager(self) -> CallbackManager:
        return CallbackManager([LLMCallbackHandler()])

    def get_llm_callback_manager(self) -> CallbackManager:
        if not self._is_llm_callback_manager_created:
            self._llm_callback_manager = self.create_llm_callback_manager()
            self._is_llm_callback_manager_created = True
        return self._llm_callback_manager

    def create_llm_prompt_template(self) -> PromptTemplate:
        return PromptTemplate(
            input_variables=["chat_history", "human_input"],
            template='\n'.join([
                'You are a chatbot having a conversation with a human.',
                '',
                '{chat_history}',
                'Human: {human_input}',
                'Chatbot:',
            ])
        )

    def get_llm_prompt_template(self) -> PromptTemplate:
        if not self._is_llm_prompt_template_created:
            self._llm_prompt_template = self.create_llm_prompt_template()
            self._is_llm_prompt_template_created = True
        return self._llm_prompt_template

    def create_llm_conversation_buffer_memory(
        self
    ) -> ConversationBufferMemory | None:
        return ConversationBufferMemory(memory_key="chat_history")

    def get_llm_conversation_buffer_memory(self) -> ConversationBufferMemory:
        if not self._is_llm_conversation_buffer_memory_created:
            self._llm_conversation_buffer_memory = self.create_llm_conversation_buffer_memory()  # noqa
            self._is_llm_conversation_buffer_memory_created = True
        return self._llm_conversation_buffer_memory

    def get_user_prompt(self) -> str:
        return self.render_str(self._user_prompt)
