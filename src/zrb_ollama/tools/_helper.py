from collections.abc import Mapping

from bs4 import BeautifulSoup


def parse_content(soup: BeautifulSoup) -> Mapping[str, str]:
    links = []
    for anchor in soup.find_all("a"):
        if not anchor or "href" not in anchor.attrs:
            continue
        link: str = anchor["href"]
        if link.startswith("#") or link.startswith("/"):
            continue
        links.append(link)
    text = soup.get_text(separator=" ", strip=True)
    return {"content": text, "links_on_page": links}
