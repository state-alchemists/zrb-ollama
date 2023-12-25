from .group import ollama_group
from .builtin import install as ollama_install
from .task.prompt_task import PromptTask

assert ollama_group
assert ollama_install
assert PromptTask
