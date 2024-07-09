from typing import Iterable
from zrb import Task
from zrb.helper.typing import Any, Callable, List, Mapping, Optional, Union
from zrb.task.any_task import AnyTask
from zrb.task.any_task_event_handler import (
    OnFailed, OnReady, OnRetry, OnSkipped, OnStarted, OnTriggered, OnWaiting
)
from zrb.task_env.env import Env
from zrb.task_env.env_file import EnvFile
from zrb.task_group.group import Group
from zrb.task_input.any_input import AnyInput
from ..agent import Agent
from ..tools import query_internet, run_shell_command


class LLMTask(Task):
    def __init__(
        self,
        name: str,
        group: Optional[Group] = None,
        description: str = "",
        inputs: List[AnyInput] = [],
        envs: Iterable[Env] = [],
        env_files: Iterable[EnvFile] = [],
        icon: Optional[str] = None,
        color: Optional[str] = None,
        retry: int = 2,
        retry_interval: float | int = 1,
        model: Optional[str] = "ollama/mistral:7b-instruct",
        system_message_template: Optional[str] = None,
        system_prompt: Optional[Any] = None,
        previous_messages: Optional[List[Any]] = None,
        tools: List[Callable] = [query_internet, run_shell_command],
        max_iteration: Union[int, str] = 10,
        agent_kwargs: Mapping[str, Any] = {},
        user_message: str = "Who are you?",
        upstreams: Iterable[AnyTask] = [],
        fallbacks: Iterable[AnyTask] = [],
        checkers: Iterable[AnyTask] = [],
        checking_interval: float | int = 0,
        on_triggered: Optional[OnTriggered] = None,
        on_waiting: Optional[OnWaiting] = None,
        on_skipped: Optional[OnSkipped] = None,
        on_started: Optional[OnStarted] = None,
        on_ready: Optional[OnReady] = None,
        on_retry: Optional[OnRetry] = None,
        on_failed: Optional[OnFailed] = None,
        should_execute: bool | str | Callable[..., bool] = True,
        return_upstream_result: bool = False
    ):
        super().__init__(
            name=name,
            group=group,
            inputs=inputs,
            envs=envs,
            env_files=env_files,
            icon=icon,
            color=color,
            description=description,
            upstreams=upstreams,
            fallbacks=fallbacks,
            on_triggered=on_triggered,
            on_waiting=on_waiting,
            on_skipped=on_skipped,
            on_started=on_started,
            on_ready=on_ready,
            on_retry=on_retry,
            on_failed=on_failed,
            checkers=checkers,
            checking_interval=checking_interval,
            retry=retry,
            retry_interval=retry_interval,
            should_execute=should_execute,
            return_upstream_result=return_upstream_result,
        )
        self._model = model
        self._system_message_template = system_message_template
        self._system_prompt = system_prompt
        self._previous_messages = previous_messages
        self._tools = tools
        self._max_iteration = max_iteration
        self._agent_kwargs = agent_kwargs
        self._user_message = user_message

    async def run(self, *args: Any, **kwargs: Any) -> Any:
        agent = Agent(
            model=self.render_str(self._model),
            system_message_template=self.render_str(self._system_message_template),
            system_prompt=self.render_str(self._system_prompt),
            previous_messages=self._previous_messages,
            tools=self._tools,
            max_iteration=self.render_int(self._max_iteration),
            print_fn=self.print_out_dark,
            **{
                self.render_str(key): self.render_any(val)
                for key, val in self._agent_kwargs.items()
            }
        )
        return agent.add_user_message(self.render_str(self._user_message))
