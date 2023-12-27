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
from zrb.config.config import default_shell
from ..config import DEFAULT_OLLAMA_BASE_URL, DEFAULT_MODEL

import asyncio
import os
import pathlib
import json
import sys
import requests


@typechecked
class PromptTask(Task):
    '''
    PromptTask sends request to ollama's Generate API (/api/generate)
    You can set options as described in ollama's modelfile parameter docs:
    https://github.com/jmorganca/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values
    '''
    def __init__(
        self,
        name: str,
        model: str = DEFAULT_MODEL,
        prompt: str | None = None,
        ollama_base_url: str = DEFAULT_OLLAMA_BASE_URL,
        context_file: str | None = None,
        executable: str | None = None,
        cwd: str | pathlib.Path | None = None,
        preexec_fn: Callable[[], Any] | None = os.setsid,
        prompt_cmd: str | None = None,
        options: Mapping[str, Any] = {},
        system_prompt: str = '',
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
        self._model = model
        self._prompt = prompt
        self._prompt_cmd = prompt_cmd
        self._ollama_base_url = ollama_base_url
        if executable is None and default_shell != '':
            executable = default_shell
        self._executable = executable
        self._preexec_fn = preexec_fn
        self.__set_cwd(cwd)
        self._options = options
        self._system_prompt = system_prompt
        self._context_file = context_file

    def __set_cwd(self, cwd: str | pathlib.Path | None):
        if cwd is None:
            self._cwd: str | pathlib.Path = os.getcwd()
            return
        self._cwd: str | pathlib.Path = os.path.abspath(cwd)

    async def run(self, *args: Any, **kwargs: Any) -> Any:
        model = self.render_str(self._model)
        base_url = self.render_str(self._ollama_base_url).rstrip('/')
        system_prompt = self.render_any(self._system_prompt)
        options = self._get_rendered_options()
        prompt = await self._get_prompt()
        context_key = '.'.join(['ollama_context', model])
        context_str = self._read_context_str(context_key)
        self.print_out_dark('Sending request...')
        payload = self._create_json_payload(
            model=model,
            options=options,
            system_prompt=system_prompt,
            prompt=prompt,
            context_str=context_str
        )
        r = requests.post(
            '/'.join([base_url, 'api/generate']),
            json=payload,
            stream=True
        )
        r.raise_for_status()
        result: str = ''
        self.print_out_dark('Waiting for response...')
        is_first_response = True
        for response in r.iter_lines():
            body = json.loads(response)
            response_part = body.get('response', '')
            if response_part != '':
                self.__print_response(response_part, is_first_response)
                is_first_response = False
                result = ''.join([result, response_part])
            if 'error' in body:
                raise Exception(body['error'])
            if body.get('done', False):
                print(file=sys.stderr, flush=True)
                context = body['context']
                context_str = json.dumps(context)
                self._write_context_str(context_key, context_str)
        return result

    def __print_response(self, response_part: str, is_first_response: bool):
        shown_response_part = '\n    '.join(response_part.split('\n'))
        if is_first_response:
            shown_response_part = ''.join(['   ', shown_response_part])
        print(
            colored(shown_response_part, attrs=['dark']),
            file=sys.stderr, end='', flush=True
        )

    def _get_rendered_options(self) -> Mapping[str, Any]:
        options = {}
        for key, value in self._options.items():
            options[key] = self.render_any(value)
        return options

    def _write_context_str(self, context_key: str, context_str: str):
        self.set_xcom(context_key, context_str)
        with open(self._context_file, 'w') as file:
            file.write(context_str)

    def _read_context_str(self, context_key: str) -> str:
        context_str = self.get_xcom(context_key)
        if context_str != '':
            return context_str
        if self._context_file is not None and self._context_file != '':
            if not os.path.isfile(self._context_file):
                return ''
            try:
                with open(self._context_file) as file:
                    return file.read()
            except Exception:
                self.print_err(f'Cannot read file: {self._context_file}')
        return ''

    def _create_json_payload(
        self,
        model: str,
        options: Mapping[str, Any],
        system_prompt: str,
        prompt: str,
        context_str: str
    ) -> Mapping[str, Any]:
        payload = {
            'model': model,
            'prompt': prompt,
            'system': system_prompt,
            'options': options
        }
        if context_str == '':
            return payload
        payload['context'] = json.loads(context_str)
        return payload

    async def _get_prompt(self):
        if self._prompt_cmd is not None and self._prompt_cmd != '':
            return await self._run_prompt_cmd()
        if self._prompt is not None:
            return self.render_str(self._prompt)
        return ''

    async def _run_prompt_cmd(self) -> str:
        cmd = self.render_str(self._prompt_cmd)
        process = await asyncio.create_subprocess_shell(
            cmd,
            cwd=self._cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=self.get_env_map(),
            shell=True,
            executable=self._executable,
            close_fds=True,
            preexec_fn=self._preexec_fn,
            bufsize=0
        )
        # Capture the standard output and error
        stdout, stderr = await process.communicate()
        # get return code
        return_code = process.returncode
        self.log_info(f'Exit status: {return_code}')
        if return_code != 0 and not self._global_state.is_killed_by_signal:
            error = stderr.decode().strip()
            raise Exception(
                f'Process {self._name} exited ({return_code}): {error}'
            )
        # Return the standard output
        return stdout.decode().strip()
