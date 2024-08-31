from collections.abc import Callable, Mapping

from ..config import INTERACTIVE_ENABLED_TOOL_NAMES
from ..tools import (
    get_current_location,
    get_current_weather,
    open_web_page,
    query_internet,
    run_shell_command,
)


class _InteractiveTools:

    def __init__(self, enabled_tool_names: list[str]):
        self._enabled_tool_names = list(enabled_tool_names)
        self._available_tools = {
            "query_internet": query_internet,
            "open_web_page": open_web_page,
            "run_shell_command": run_shell_command,
            "get_current_location": get_current_location,
            "get_current_weather": get_current_weather,
        }

    def register(self, *tools: Callable):
        for tool in tools:
            tool_name = tool.__name__
            self._available_tools[tool_name] = tool
            if tool_name not in self._enabled_tool_names:
                self._enabled_tool_names.append(tool_name)

    def get_available_tools(self) -> Mapping[str, Callable]:
        return self._available_tools

    def get_enabled_tool_names(self) -> list[str]:
        return self._enabled_tool_names


interactive_tools = _InteractiveTools(enabled_tool_names=INTERACTIVE_ENABLED_TOOL_NAMES)
