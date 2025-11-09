import re
import requests
from bs4 import BeautifulSoup
from typing import Tuple, List, Dict

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

WIKI_MAIN_SELECTOR = "#mw-content-text"


def _clean_text(text: str) -> str:
    text = re.sub(r"\[\d+\]", "", text)  # remove citation refs like [1], [2]
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _extract_summary(paragraphs: List[str]) -> str:
    summary = []
    for p in paragraphs:
        if len(summary) >= 3:
            break
        if len(p.split()) > 20:
            summary.append(p)
    return " ".join(summary)


def _extract_sections(soup: BeautifulSoup) -> List[str]:
    sections = []
    for tag in soup.select("h2 .mw-headline, h3 .mw-headline"):
        txt = tag.get_text(strip=True)
        if txt.lower() not in ["references", "external links", "see also"]:
            sections.append(txt)
    return sections[:10]


def _extract_entities(text: str) -> Dict[str, List[str]]:
    words = set(text.split())
    # Very lightweight fake NER - just return capitalized keywords
    candidates = [w.strip(",.") for w in words if w.istitle() and len(w) > 3]
    return {
        "people": candidates[:10],
        "organizations": [],
        "locations": []
    }


def scrape_wikipedia(url: str):
    """
    Returns:
      title,
      summary,
      sections,
      key_entities,
      full_cleaned_text
    """
    if not url.startswith(("http://", "https://")):
        raise ValueError("URL must start with http:// or https://")

    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    title_tag = soup.find("h1", id="firstHeading")
    title = title_tag.get_text(strip=True) if title_tag else soup.title.get_text(strip=True)

    content_root = soup.select_one(WIKI_MAIN_SELECTOR)
    if not content_root:
        raise RuntimeError("Could not locate Wikipedia main content")

    for selector in ["table", ".infobox", ".navbox", ".vertical-navbox", ".toc", ".reflist"]:
        for tag in content_root.select(selector):
            tag.decompose()

    for sup in content_root.find_all("sup"):
        sup.decompose()

    paragraphs = [p.get_text(" ", strip=True) for p in content_root.find_all("p") if p.get_text(strip=True)]
    lists = [li.get_text(" ", strip=True) for li in content_root.find_all("li")]

    text_blocks = paragraphs + lists
    clean_text = _clean_text("\n".join(text_blocks))

    summary = _extract_summary(paragraphs)
    sections = _extract_sections(content_root)
    key_entities = _extract_entities(summary or clean_text)

    return title, summary, sections, key_entities, clean_text
