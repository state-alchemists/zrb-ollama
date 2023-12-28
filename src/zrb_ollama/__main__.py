from zrb import Task, python_task
from zrb.helper.typing import Any, List
from zrb.helper.accessories.color import colored
from .builtin.install import install
from .task.prompt_task import PromptTask
from .config import DEFAULT_MODEL, DEFAULT_OLLAMA_BASE_URL, VERBOSE_EVAL

import os
import subprocess
import threading
import sys

_LOCAL_OLLAMA_BASE_URLS = (
    'http://localhost:11434', 'http://0.0.0.0:11434', 'http://127.0.0.1:11434'
)
_HOME_DIR = os.path.expanduser('~')


def vanilla_prompt():
    prompt = _get_user_prompt()
    prompt_task = _create_prompt_task(prompt=prompt)
    prompt_fn = prompt_task.to_function()
    prompt_fn()


def python_prompt():
    prompt = _get_user_prompt()
    prompt_task = _create_prompt_task(
        prompt=prompt,
        system_prompt='\n'.join([
            "You are a Python code generator.",
            "Your task is to interpret the user's input as a Python coding task and generate a Python code that fulfills the request.",  # noqa
            "The code should be ready to run in a Python interpreter without any additional preprocessing.",  # noqa
            "Focus on generating concise and correct Python code for each task.",  # noqa
            "Always ensure that the code is safe to run and adheres to Python best practices.",  # noqa
            "Make sure you only produce Python code, no explanation is needed. Just Python.",  # noqa
        ]),
    )
    eval_task = _create_eval_task(
        upstreams=[prompt_task],
        xcom_key='prompt'
    )
    eval_fn = eval_task.to_function()
    eval_fn()


def _create_prompt_task(
    prompt: str = '',
    system_prompt: str = '',
    context_file: str = ''
) -> Task:
    if context_file == '':
        context_file = os.path.join(
            _HOME_DIR, '.zrb-ollama-context.json'
        )
    prompt_task = PromptTask(
        name='prompt',
        icon='🦙',
        color='light_green',
        ollama_base_url=DEFAULT_OLLAMA_BASE_URL,
        model=DEFAULT_MODEL,
        system_prompt=system_prompt,
        prompt=prompt,
        context_file=context_file
    )
    if DEFAULT_OLLAMA_BASE_URL.rstrip('/') in _LOCAL_OLLAMA_BASE_URLS:
        prompt_task.add_upstream(install)
    return prompt_task


def _get_user_prompt():
    if len(sys.argv) > 1:
        return ' '.join(sys.argv[1:])
    return 'Tell me some random fun facts'


def _create_eval_task(upstreams: List[Task], xcom_key: str) -> Task:
    @python_task(
        name='evaluate',
        icon='✏️',
        color='green',
        upstreams=upstreams,
        retry=0
    )
    def evaluate(*args, **kwargs):
        task: Task = kwargs.get('_task')
        python_script = _extract_python_script(task.get_xcom(xcom_key))
        shown_lines = python_script.split('\n')
        if VERBOSE_EVAL:
            task.print_out_dark('\n    '.join(['Evaluating:', *shown_lines]))
        process = subprocess.Popen(
            ['python', '-c', python_script],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        task.print_out_dark('Waiting for evaluation...')
        stdout_lines, stderr_lines = [], []
        stdout_thread = threading.Thread(
            target=_print_stream, args=(process.stdout, stdout_lines)
        )
        stderr_thread = threading.Thread(
            target=_print_stream, args=(process.stderr, stderr_lines)
        )
        stdout_thread.start()
        stderr_thread.start()
        process.wait()
        stdout_thread.join()
        stderr_thread.join()
        if process.returncode != 0:
            raise Exception(f'Non zero exit code: {process.returncode}')
        return ''.join(stdout_lines)
    return evaluate


def _extract_python_script(response: str) -> str:
    response = response.lstrip().rstrip()
    if '```python' in response:
        lines = response.split('\n')
        is_code = False
        codes = []
        for line in lines:
            if line == '```python':
                is_code = True
                continue
            if is_code and line == '```':
                break
            if is_code:
                codes.append(line)
        return '\n'.join(codes)
    return response


def _print_stream(stream: Any, lines: List[str]):
    while True:
        line = stream.readline()
        if not line:
            break
        print(
            colored(line, attrs=['dark']), end='', file=sys.stderr, flush=True
        )
        lines.append(line)
