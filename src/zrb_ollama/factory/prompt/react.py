from langchain.prompts import PromptTemplate
from langchain_core.prompts import BasePromptTemplate

from ...config import SYSTEM_PROMPT, REACT_PROMPT
from ...task.any_prompt_task import AnyPromptTask
from ..schema import PromptFactory


def react_prompt_factory(
    react_prompt: str = REACT_PROMPT,
    system_prompt: str = SYSTEM_PROMPT
) -> PromptFactory:
    def create_prompt(task: AnyPromptTask) -> BasePromptTemplate:
        return PromptTemplate.from_template(
            "\n".join([
                task.render_str(system_prompt),
                "",
                react_prompt,
            ])
        )

    return create_prompt
