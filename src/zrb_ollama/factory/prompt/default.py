from ...config import DEFAULT_SYSTEM_PROMPT
from ..schema import PromptFactory


def default_prompt_factory(system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> PromptFactory:
    from .react import react_prompt_factory

    return react_prompt_factory(system_prompt=system_prompt)
