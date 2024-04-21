from ...config import SYSTEM_PROMPT, REACT_PROMPT
from ..schema import PromptFactory


def default_prompt_factory(
    react_prompt: str = REACT_PROMPT,
    system_prompt: str = SYSTEM_PROMPT
) -> PromptFactory:
    from .react import react_prompt_factory

    return react_prompt_factory(
        react_prompt=react_prompt, system_prompt=system_prompt
    )
