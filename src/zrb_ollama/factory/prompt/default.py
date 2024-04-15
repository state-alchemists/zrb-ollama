from ...config import SYSTEM_PROMPT
from ..schema import PromptFactory


def default_prompt_factory(system_prompt: str = SYSTEM_PROMPT) -> PromptFactory:
    from .react import react_prompt_factory

    return react_prompt_factory(system_prompt=system_prompt)
