import requests
from bs4 import BeautifulSoup


def query_internet(query: str, num_results: int = 10) -> str:
    """Search factual information from the internet."""
    response = requests.get(
        "https://google.com/search",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"  # noqa
        },
        params={
            "q": query,
            "num": num_results,
        }
    )
    if response.status_code != 200:
        raise Exception(
            f"Error: Unable to retrieve search results (status code: {response.status_code})"  # noqa
        )
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()
