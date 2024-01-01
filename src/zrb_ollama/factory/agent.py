from langchain.agents import Agent, ZeroShotAgent
from .schema import AgentFactory
from ..task.any_prompt_task import AnyPromptTask


def agent_factory(verbose: bool = False) -> AgentFactory:
    def create_agent(task: AnyPromptTask) -> Agent:
        return ZeroShotAgent(
            llm_chain=task.get_agent_llm_chain(),
            tools=task.get_agent_tools(),
            verbose=verbose,
        )
    return create_agent
