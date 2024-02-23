import sys
from typing import Mapping, Callable

import requests
from bs4 import BeautifulSoup
from langchain.agents import Tool
from langchain_core.tools import BaseTool
from readability import Document  # Corrected import statement
from zrb.helper.accessories.color import colored

from zrb_ollama.factory.schema import ToolFactory
from zrb_ollama.task.any_prompt_task import AnyPromptTask


def search_tool_factory(
    name: str = "Search Engine",
    description: str ="Use this tool to lookup information from search engine. Input should be the query.",  # noqa
    max_results: str | int = 5
) -> ToolFactory:
    def create_search_tool(task: AnyPromptTask) -> BaseTool:
        return Tool(
            name=task.render_str(name),
            description=task.render_str(description),
            func=_create_search_duckduckgo(max_results=task.render_int(max_results)),
        )

    return create_search_tool


def _create_search_duckduckgo(max_results: int) -> Callable[[str], str]:
    def search_duckduckgo(keyword: str) -> str:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"  # noqa
        }
        params = {"q": keyword, "kl": "wt-wt", "kp": "-1"}
        response = requests.get(
            "https://duckduckgo.com/html/", params=params, headers=headers
        )
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            result_urls = [a["href"] for a in soup.select(".result__a")]
            results = []
            result_count = 0
            for url in result_urls:
                if result_count >= max_results:
                    break
                main_content = _extract_main_content(url, headers)
                if main_content != "":
                    print(
                        colored(main_content, attrs=["dark"]),
                        file=sys.stderr,
                        flush=True,
                    )
                    results.append(main_content)
                    result_count += 1
            return "\n".join(results)
        else:
            raise Exception("Failed to search DuckDuckGo.")
    return search_duckduckgo


def _extract_main_content(url: str, headers: Mapping[str, str]):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Use readability-lxml's Document for extracting main content
            doc = Document(response.text)
            summary = doc.summary()
            # Convert summary (HTML content) to text if needed
            soup_summary = BeautifulSoup(summary, "html.parser")
            text_summary = soup_summary.get_text().strip()
            return f"Content from {url}:\n{text_summary}"
        return ""
    except Exception:
        return ""

