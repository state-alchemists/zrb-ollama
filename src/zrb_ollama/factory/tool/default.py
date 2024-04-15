from typing import List

from ..schema import ToolFactory


def default_tool_factories() -> List[ToolFactory]:
    from .bash_repl import bash_repl_tool_factory
    from .python_repl import python_repl_tool_factory
    from .search import search_tool_factory

    factories: List[ToolFactory] = [
        search_tool_factory(),
        bash_repl_tool_factory(),
        python_repl_tool_factory(),
    ]
    return factories
