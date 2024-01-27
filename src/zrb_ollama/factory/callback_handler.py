import sys

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.callbacks.base import BaseCallbackHandler
from zrb.helper.accessories.color import colored
from zrb.helper.typing import Any

from zrb_ollama.factory.schema import CallbackHandlerFactory
from zrb_ollama.task.any_prompt_task import AnyPromptTask


class _DefaultCallbackHandler(StreamingStdOutCallbackHandler):
    def __init__(self) -> None:
        super().__init__()
        self._is_first_token = True

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        shown_text = "\n    ".join(token.split("\n"))
        if self._is_first_token:
            shown_text = "".join(["    ", shown_text])
        print(colored(shown_text, attrs=["dark"]), file=sys.stderr, end="", flush=True)
        self._is_first_token = False


def default_callback_handler_factory() -> CallbackHandlerFactory:
    def create_callback_handler(task: AnyPromptTask) -> BaseCallbackHandler:
        return _DefaultCallbackHandler()

    return create_callback_handler
