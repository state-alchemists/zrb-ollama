from langchain.agents import AgentExecutor
from .schema import AgentExecutorFactory
from ..task.any_prompt_task import AnyPromptTask


def agent_executor_factory(
    verbose: bool = False, handle_parsing_errors: bool = True
) -> AgentExecutorFactory:
    def create_agent_executor(task: AnyPromptTask) -> AgentExecutor:
        return AgentExecutor.from_agent_and_tools(
            agent=task.get_agent(),
            tools=task.get_agent_tools(),
            verbose=verbose,
            memory=task.get_chat_memory(),
            handle_parsing_errors=handle_parsing_errors
        )
    return create_agent_executor
