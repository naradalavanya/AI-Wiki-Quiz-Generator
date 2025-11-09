import re
import requests
from bs4 import BeautifulSoup
from typing import Tuple

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"}
WIKI_MAIN_SELECTOR = "#mw-content-text"

def _clean_text(text: str) -> str:
    # Remove footnote markers like [1], [2], collapse whitespace
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def scrape_wikipedia(url: str) -> Tuple[str, str]:
    """Return (title, clean_text) for a Wikipedia article URL."""
    if not (url.startswith("http://") or url.startswith("https://")):
        raise ValueError("URL must start with http:// or https://")

    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Title
    title_tag = soup.find("h1", id="firstHeading")
    title = title_tag.get_text(strip=True) if title_tag else (soup.title.get_text(strip=True) if soup.title else "Wikipedia Article")

    # Main content
    content_root = soup.select_one(WIKI_MAIN_SELECTOR)
    if not content_root:
        raise RuntimeError("Could not locate Wikipedia main content")

    # Remove tables, infoboxes, navboxes, ToC, references list
    for selector in ["table", ".infobox", ".navbox", ".vertical-navbox", ".toc", ".reflist"]:
        for tag in content_root.select(selector):
            tag.decompose()

    # Remove superscripts (citation markers)
    for sup in content_root.find_all("sup"):
        sup.decompose()

    # Collect paragraph + list item text
    paragraphs = [p.get_text(" ", strip=True) for p in content_root.find_all(["p", "li"]) if p.get_text(strip=True)]
    clean = _clean_text("\n".join(paragraphs))

    return title, clean
