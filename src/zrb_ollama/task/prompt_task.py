from zrb.helper.typecheck import typechecked
from zrb.helper.typing import Callable, Iterable, List
from zrb.task.any_task import AnyTask
from zrb.task.any_task_event_handler import (
    OnFailed, OnReady, OnRetry, OnSkipped, OnStarted, OnTriggered, OnWaiting
)
from zrb.task_env.env import Env
from zrb.task_env.env_file import EnvFile
from zrb.task_group.group import Group
from zrb.task_input.any_input import AnyInput
from ..config import DEFAULT_OLLAMA_BASE_URL, DEFAULT_MODEL
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.chat_models import ChatOllama
from .langchain_task import LLMTask


@typechecked
class PromptTask(LLMTask):
    '''
    PromptTask sends request to ollama's Generate API (/api/generate)
    You can set options as described in ollama's modelfile parameter docs:
    https://github.com/jmorganca/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values
    '''
    def __init__(
        self,
        name: str,
        prompt: str,
        history_file: str | None = None,
        ollama_base_url: str = DEFAULT_OLLAMA_BASE_URL,
        ollama_model: str = DEFAULT_MODEL,
        ollama_mirostat: int | str | None = None,
        ollama_mirostat_eta: float | str | None = None,
        ollama_mirostat_tau: float | str | None = None,
        ollama_num_ctx: int | str | None = None,
        ollama_num_gpu: int | str | None = None,
        ollama_num_thread: int | str | None = None,
        ollama_repeat_last_n: int | str | None = None,
        ollama_repeat_penalty: float | str | None = None,
        ollama_temperature: float | str | None = None,
        ollama_stop: List[str] | None = None,
        ollama_tfs_z: float | str | None = None,
        ollama_top_k: int | str | None = None,
        ollama_top_p: int | str | None = None,
        ollama_system: str | str | None = None,
        ollama_template: str | str | None = None,
        ollama_format: str | str | None = None,
        ollama_timeout: int | str | None = None,
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
            prompt=prompt,
            history_file=history_file,
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
        self._ollama_base_url = ollama_base_url,
        self._ollama_model = ollama_model
        self._ollama_mirostat = ollama_mirostat
        self._ollama_mirostat_eta = ollama_mirostat_eta
        self._ollama_mirostat_tau = ollama_mirostat_tau
        self._ollama_num_ctx = ollama_num_ctx
        self._ollama_num_gpu = ollama_num_gpu
        self._ollama_num_thread = ollama_num_thread
        self._ollama_repeat_last_n = ollama_repeat_last_n
        self._ollama_repeat_penalty = ollama_repeat_penalty
        self._ollama_temperature = ollama_temperature
        self._ollama_stop = ollama_stop
        self._ollama_tfs_z = ollama_tfs_z
        self._ollama_top_k = ollama_top_k
        self._ollama_top_p = ollama_top_p
        self._ollama_system = ollama_system
        self._ollama_template = ollama_template
        self._ollama_format = ollama_format
        self._ollama_timeout = ollama_timeout

    def create_chat_model(self) -> BaseChatModel:
        return ChatOllama(
            model=self.render_str(self._ollama_model),
            mirostat=self.render_any(self._ollama_mirostat),
            mirostat_eta=self.render_any(self._ollama_mirostat_eta),
            mirostat_tau=self.render_any(self._ollama_mirostat_tau),
            num_ctx=self.render_any(self._ollama_num_ctx),
            num_gpu=self.render_any(self._ollama_num_gpu),
            num_thread=self.render_any(self._ollama_num_thread),
            repeat_last_n=self.render_any(self._ollama_repeat_last_n),
            repeat_penalty=self.render_any(self._ollama_repeat_penalty),
            temperature=self.render_any(self._ollama_temperature),
            stop=self.render_any(self._ollama_stop),
            tfs_z=self.render_any(self._ollama_tfs_z),
            top_k=self.render_any(self._ollama_top_k),
            top_p=self.render_any(self._ollama_top_p),
            system=self.render_any(self._ollama_system),
            template=self.render_any(self._ollama_template),
            format=self.render_any(self._ollama_format),
            timeout=self.render_any(self._ollama_timeout),
            callback_manager=self.get_callback_manager(),
        )
