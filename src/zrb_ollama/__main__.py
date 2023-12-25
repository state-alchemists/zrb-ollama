from .task.prompt_task import PromptTask
from .config import DEFAULT_MODEL
import sys


def main():
    task = PromptTask(
        name='prompt',
        model=DEFAULT_MODEL,
        prompt=_get_prompt()
    )
    fn = task.to_function()
    fn()


def _get_prompt():
    if len(sys.argv) > 1:
        return ' '.join(sys.argv[1:])
    return 'Tell me some random fun facts'
