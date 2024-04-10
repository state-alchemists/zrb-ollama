from .builtin import install_ollama
from .factory.schema import (
    CallbackHandlerFactory,
    LLMFactory,
    PromptFactory,
    ToolFactory,
)
from .group import ollama_group
from .task import AnyPromptTask, PromptTask

assert ollama_group
assert install_ollama
assert AnyPromptTask
assert PromptTask

assert CallbackHandlerFactory
assert LLMFactory
assert ToolFactory
assert PromptFactory
