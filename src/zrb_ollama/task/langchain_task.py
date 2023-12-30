from functools import lru_cache
from zrb import Task
from zrb.helper.typecheck import typechecked
from zrb.helper.typing import Any, Callable, Iterable, List, Mapping
from zrb.helper.accessories.color import colored
from zrb.task.any_task import AnyTask
from zrb.task.any_task_event_handler import (
    OnFailed, OnReady, OnRetry, OnSkipped, OnStarted, OnTriggered, OnWaiting
)
from zrb.task_env.env import Env
from zrb.task_env.env_file import EnvFile
from zrb.task_group.group import Group
from zrb.task_input.any_input import AnyInput
from ..config import DEFAULT_MODEL, DEFAULT_OLLAMA_BASE_URL
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.chat_models import ChatOllama
from langchain.memory.chat_memory import BaseChatMemory
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
)
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import (
    StreamingStdOutCallbackHandler
)

import os
import json
import sys


class ZrbStderrCallbackHandler(StreamingStdOutCallbackHandler):

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
        self._history_file_name = history_file

    async def run(self, *args: Any, **kwargs: Any) -> Any:
        chain = self.get_llm_chain()
        user_prompt = self.get_rendered_user_prompt()
        llm_response = chain.run(user_prompt)
        self.save_chat_context(input=user_prompt, output=llm_response)
        return llm_response

    @lru_cache(maxsize=1)
    def get_llm_chain(self) -> LLMChain:
        return self.create_llm_chain()

    def create_llm_chain(self) -> LLMChain:
        return LLMChain(
            llm=self.get_chat_model(),
            prompt=self.get_chat_prompt_template(),
            memory=self.get_chat_memory(),
            verbose=False
        )

    @lru_cache(maxsize=1)
    def get_callback_manager(self) -> CallbackManager:
        return self.create_callback_manager()

    def create_callback_manager(self) -> CallbackManager:
        return CallbackManager([ZrbStderrCallbackHandler()])

    @lru_cache(maxsize=1)
    def get_chat_model(self) -> BaseChatModel:
        return self.create_chat_model()

    def create_chat_model(self) -> BaseChatModel:
        return ChatOllama(
            model=DEFAULT_MODEL,
            base_url=DEFAULT_OLLAMA_BASE_URL,
            callback_manager=self.get_callback_manager(),
        )

    @lru_cache(maxsize=1)
    def get_chat_prompt_template(self) -> ChatPromptTemplate:
        return self.create_chat_prompt_template()

    def create_chat_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate(
            messages=[
                # The `variable_name` here is what must align with memory
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}"),
            ]
        )

    @lru_cache(maxsize=1)
    def get_chat_memory(self) -> BaseChatMemory:
        return self.create_chat_memory()

    def create_chat_memory(self) -> BaseChatMemory:
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
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
