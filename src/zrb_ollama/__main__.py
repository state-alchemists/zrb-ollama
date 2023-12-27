from zrb import Task, python_task
from zrb.helper.typing import Any, List
from .builtin.install import install
from .task.prompt_task import PromptTask
from .config import DEFAULT_MODEL, DEFAULT_OLLAMA_BASE_URL

import os
import subprocess
import threading
import sys

_LOCAL_OLLAMA_BASE_URLS = (
    'http://localhost:11434', 'http://0.0.0.0:11434', 'http://127.0.0.1:11434'
)
_HOME_DIR = os.path.expanduser('~')


def vanilla_prompt():
    prompt_task = _create_prompt_task()
    prompt_fn = prompt_task.to_function()
    prompt_fn()


def python_prompt():
    prompt_task = _create_prompt_task(
        system_prompt='\n'.join([
            "You are a Python code generator.",
            "Your task is to interpret the user's input as a Python coding task and generate a Python code that fulfills the request.",  # noqa
            "The code should be ready to run in a Python interpreter without any additional preprocessing.",  # noqa
            "Focus on generating concise and correct Python code for each task.",  # noqa
            "Always ensure that the code is safe to run and adheres to Python best practices.",  # noqa
            "Make sure you only produce Python code, no explanation is needed. Just Python.",  # noqa
        ]),
        context_suffix='py'
    )

    @python_task(
        name='eval',
        upstreams=[prompt_task]
    )
    def evaluate(*args, **kwargs):
        task: Task = kwargs.get('_task')
        python_script = _extract_python_script(task.get_xcom('prompt'))
        shown_lines = python_script.split('\n')
        task.print_out_dark('\n    '.join(['Evaluating:', *shown_lines]))
        process = subprocess.Popen(
            ['python', '-c', python_script],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
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

    evaluate_fn = evaluate.to_function()
    evaluate_fn()


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
        print(line, end='', file=sys.stderr, flush=True)
        lines.append(line)


def _create_prompt_task(
    system_prompt: str = '',
    context_suffix: str = ''
) -> Task:
    context_file_name = '.zrb-ollama-context'
    if context_suffix != '':
        context_file_name = '-'.join([
            context_file_name, context_suffix
        ])
    context_file_name = '.'.join([context_file_name, 'json'])
    prompt_task = PromptTask(
        name='prompt',
        icon='🦙',
        color='green',
        ollama_base_url=DEFAULT_OLLAMA_BASE_URL,
        model=DEFAULT_MODEL,
        system_prompt=system_prompt,
        prompt=_get_user_prompt(),
        context_file=os.path.join(_HOME_DIR, context_file_name)
    )
    if DEFAULT_OLLAMA_BASE_URL.rstrip('/') in _LOCAL_OLLAMA_BASE_URLS:
        prompt_task.add_upstream(install)
    return prompt_task


def _get_user_prompt():
    if len(sys.argv) > 1:
        return ' '.join(sys.argv[1:])
    return 'Tell me some random fun facts'
