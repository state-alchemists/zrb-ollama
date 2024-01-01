from langchain.prompts import PromptTemplate
from langchain.agents import ZeroShotAgent
from .schema import PromptTemplateFactory
from ..task.any_prompt_task import AnyPromptTask


def agent_prompt_template_factory() -> PromptTemplateFactory:
    def create_agent_prompt_template(task: AnyPromptTask) -> PromptTemplate:
        return ZeroShotAgent.create_prompt(
            tools=task.get_agent_tools(),
            prefix=_get_prompt_prefix(task),
            suffix='\n'.join([
                'Begin!',
                '{chat_history}',
                '',
                'Question: {question}',
                '{agent_scratchpad}'
            ]),
            input_variables=["question", "chat_history", "agent_scratchpad"],
        )
    return create_agent_prompt_template


def _get_prompt_prefix(task: AnyPromptTask):
    prompt_prefix = 'You have access to the following tools:'
    rendered_system_prompt = task.get_rendered_system_prompt()
    if rendered_system_prompt is not None:
        prompt_prefix = '\n'.join([
            rendered_system_prompt,
            prompt_prefix
        ])
    return prompt_prefix
