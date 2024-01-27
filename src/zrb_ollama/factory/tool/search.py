from langchain.agents import Tool
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain_core.tools import BaseTool

from zrb_ollama.factory.schema import ToolFactory
from zrb_ollama.task.any_prompt_task import AnyPromptTask


def search_tool_factory(
    name: str = "Search",
    description="Search engine to answer questions about current events",
    region: str | None = "wt-wt",
    safesearch: str = "moderate",
    time: str | None = "y",
    max_results: int = 5,
    backend: str = "api",
    source: str = "text",
) -> ToolFactory:
    def create_search_tool(task: AnyPromptTask) -> BaseTool:
        search = DuckDuckGoSearchAPIWrapper(
            region=task.render_str(region),
            safesearch=task.render_str(safesearch),
            time=task.render_str(time),
            max_results=task.render_int(max_results),
            backend=task.render_str(backend),
            source=task.render_str(source),
        )
        return Tool(
            name=task.render_str(name),
            description=task.render_str(description),
            func=search.run,
        )

    return create_search_tool
