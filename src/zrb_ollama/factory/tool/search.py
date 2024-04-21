import sys
from typing import Callable, Mapping
from functools import lru_cache

import requests
from bs4 import BeautifulSoup
from langchain.agents import Tool
from langchain_core.tools import BaseTool
from readability import Document
from zrb.helper.accessories.color import colored

from ...task.any_prompt_task import AnyPromptTask
from ..schema import ToolFactory
from ...config import MAX_SEARCH_CHAR_LENGTH, MAX_SEARCH_RESULT

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"  # noqa
}


def search_tool_factory(
    name: str = "Search Engine",
    description: str = "Use this tool to lookup factual/up-to-date information from the internet. The input should be the search query.",  # noqa
    max_results: str | int = MAX_SEARCH_RESULT,
    max_char_length: str | int = MAX_SEARCH_CHAR_LENGTH,
) -> ToolFactory:
    def create_search_tool(task: AnyPromptTask) -> BaseTool:
        return Tool(
            name=task.render_str(name),
            description=task.render_str(description),
            func=_create_search_duckduckgo(
                max_results=task.render_int(max_results),
                max_char_length=task.render_int(max_char_length),
            ),
            handle_tool_error=True,
        )

    return create_search_tool


def _create_search_duckduckgo(
    max_results: int,
    max_char_length: int,
) -> Callable[[str], str]:
    @lru_cache
    def search_duckduckgo(keyword: str) -> str:
        params = {"q": keyword, "kl": "wt-wt", "kp": "-1"}
        response = requests.get(
            "https://duckduckgo.com/html/", params=params, headers=_HEADERS
        )
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            result_urls = [a["href"] for a in soup.select(".result__a")]
            result_count = 0
            return_value = ""
            for url in result_urls:
                if (
                    result_count >= max_results or len(return_value) >= max_char_length
                ):  # noqa
                    break
                main_content = _extract_main_content(url)
                print(colored(f"Fetching URL: {url}", attrs=["dark"]))
                if main_content != "":
                    print(
                        colored(main_content, attrs=["dark"]),
                        file=sys.stderr,
                        flush=True,
                    )
                    return_value = f"{return_value}\n{main_content}"
                    result_count += 1
            return return_value[:max_char_length]
        else:
            raise Exception("Failed to search DuckDuckGo.")

    return search_duckduckgo


@lru_cache
def _extract_main_content(url: str):
    try:
        response = requests.get(url, headers=_HEADERS)
        if response.status_code == 200:
            # Use readability-lxml's Document for extracting main content
            doc = Document(response.text)
            summary = doc.summary()
            # Convert summary (HTML content) to text if needed
            soup_summary = BeautifulSoup(summary, "html.parser")
            return soup_summary.get_text().strip()
        return ""
    except Exception:
        return ""
