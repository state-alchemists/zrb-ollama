from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import BasePromptTemplate
from langchain_core.tools import BaseTool
from zrb.helper.typing import Callable

from zrb_ollama.task.any_prompt_task import AnyPromptTask

CallbackHandlerFactory = Callable[[AnyPromptTask], BaseCallbackHandler]
LLMFactory = Callable[[AnyPromptTask], BaseLanguageModel]
ToolFactory = Callable[[AnyPromptTask], BaseTool]
PromptFactory = Callable[[AnyPromptTask], BasePromptTemplate]
