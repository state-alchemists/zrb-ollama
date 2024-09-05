from collections.abc import Callable, Mapping
from typing import Any, Iterable, Optional, Union

from zrb import AnyTask, Task
from zrb.task.any_task_event_handler import (
    OnFailed,
    OnReady,
    OnRetry,
    OnSkipped,
    OnStarted,
    OnTriggered,
    OnWaiting,
)
from zrb.task_env.env import Env
from zrb.task_env.env_file import EnvFile
from zrb.task_group.group import Group
from zrb.task_input.any_input import AnyInput

from ..agent import Agent
from ..tools import query_internet, run_shell_command


class ToolFactory:
    def __init__(self, factory: Callable[..., Any], *args: Any, **kwargs: Any):
        self._factory = factory
        self._args = args
        self._kwargs = kwargs
        self._task: Optional[AnyTask] = None

    def set_task(self, task: AnyTask):
        self._task = task

    def get_tool(self):
        args = [self._task.render_anY(arg) for arg in self._args]
        kwargs = {
            self._task.render_str(key): self._task.render_any(value)
            for key, value in self._kwargs.items()
        }
        return self._factory(*args, **kwargs)


class LLMTask(Task):
    def __init__(
        self,
        name: str,
        group: Optional[Group] = None,
        description: str = "",
        inputs: list[AnyInput] = [],
        envs: Iterable[Env] = [],
        env_files: Iterable[EnvFile] = [],
        icon: Optional[str] = None,
        color: Optional[str] = None,
        retry: int = 2,
        retry_interval: float | int = 1,
        model: Optional[str] = None,
        system_message_template: Optional[str] = None,
        system_prompt: Optional[Any] = None,
        json_fixer_system_message_template: Optional[str] = None,
        json_fixer_system_prompt: Optional[Any] = None,
        previous_messages: Optional[list[Any]] = None,
        tools: Iterable[Callable] = [query_internet, run_shell_command],
        tool_factories: Iterable[ToolFactory] = [],
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
        return_upstream_result: bool = False,
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
        self._json_fixer_system_message_template = json_fixer_system_message_template
        self._json_fixer_system_prompt = json_fixer_system_prompt
        self._previous_messages = previous_messages
        self._tools = tools
        for factory in tool_factories:
            factory.set_task(self)
        self._tool_factories = tool_factories
        self._max_iteration = max_iteration
        self._agent_kwargs = agent_kwargs
        self._user_message = user_message

    async def run(self, *args: Any, **kwargs: Any) -> Any:
        agent = Agent(
            model=self.render_str(self._model),
            system_message_template=self.render_str(self._system_message_template),
            system_prompt=self.render_str(self._system_prompt),
            json_fixer_system_message_template=self.render_str(
                self._json_fixer_system_message_template
            ),
            json_fixer_system_prompt=self.render_str(self._json_fixer_system_prompt),
            previous_messages=self._previous_messages,
            tools=self._tools
            + [factory.get_tool() for factory in self._tool_factories],
            max_iteration=self.render_int(self._max_iteration),
            print_fn=self.print_out_dark,
            **{
                self.render_str(key): self.render_any(val)
                for key, val in self._agent_kwargs.items()
            }
        )
        return await agent.add_user_message(self.render_str(self._user_message))
