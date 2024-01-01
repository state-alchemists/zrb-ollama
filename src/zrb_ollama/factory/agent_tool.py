from zrb.helper.typing import Callable, Any
from langchain.agents import Tool
from .schema import AgentToolFactory
from ..task.any_prompt_task import AnyPromptTask


def agent_tool_factory(
    name: str, description: str, func: Callable[..., Any] | None, **kwargs: Any
) -> AgentToolFactory:
    def create_agent_tool(task: AnyPromptTask) -> Tool:
        return Tool(
            name=task.render_str(name),
            func=func,
            description=task.render_str(description),
            **kwargs
        )
    return create_agent_tool


def duckduckgo_search_agent_tool_factory(
    name: str = 'duckduckgo_search',
    description: str = 'Useful to answer questions about current events',
    region: str | None = 'wt-wt',
    safesearch: str = 'moderate',
    time: str | None = 'y',
    max_results: int = 5,
    backend: str = 'api',
    source: str = 'text',
) -> AgentToolFactory:
    def create_duckduckgo_search_agent_tool(task: AnyPromptTask) -> Tool:
        from langchain_community.utilities.duckduckgo_search import (
            DuckDuckGoSearchAPIWrapper
        )
        search = DuckDuckGoSearchAPIWrapper(
            region=region,
            safesearch=safesearch,
            time=time,
            max_results=max_results,
            backend=backend,
            source=source
        )
        create_agent_tool = agent_tool_factory(
            name=name, func=search.run, description=description
        )
        return create_agent_tool(task)
    return create_duckduckgo_search_agent_tool


def python_repl_agent_tool_factory(
    name: str = 'python_repl',
    description: str = 'A Python shell. Use this to execute python code. Input should be a valid python code. If you want to see the output of a value, you should print it out with `print(...)`.',  # noqa
) -> AgentToolFactory:
    def create_python_repl_agent_tool(task: AnyPromptTask) -> Tool:
        from .helper.python_repl import eval_python
        create_agent_tool = agent_tool_factory(
            name=name, func=eval_python, description=description
        )
        return create_agent_tool(task)
    return create_python_repl_agent_tool
