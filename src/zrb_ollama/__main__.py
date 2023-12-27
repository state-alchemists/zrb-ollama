from .builtin.install import install
from .task.prompt_task import PromptTask
from .config import DEFAULT_MODEL, DEFAULT_OLLAMA_BASE_URL
import os
import sys

_LOCAL_OLLAMA_BASE_URLS = (
    'http://localhost:1143',
    'http://0.0.0.0:1143',
    'http://127.0.0.1:1143',
)

_HOME_DIR = os.path.expanduser('~')


def main():
    if DEFAULT_OLLAMA_BASE_URL.rstrip('/') in _LOCAL_OLLAMA_BASE_URLS:
        _install_ollama()
    prompt = PromptTask(
        name='prompt',
        icon='🦙',
        color='green',
        ollama_base_url=DEFAULT_OLLAMA_BASE_URL,
        model=DEFAULT_MODEL,
        prompt=_get_prompt(),
        context_file=os.path.join(_HOME_DIR, '.zrb-ollama-context.json')
    )
    prompt_fn = prompt.to_function()
    prompt_fn()


def _install_ollama():
    install_fn = install.to_function()
    install_fn()


def _get_prompt():
    if len(sys.argv) > 1:
        return ' '.join(sys.argv[1:])
    return 'Tell me some random fun facts'
