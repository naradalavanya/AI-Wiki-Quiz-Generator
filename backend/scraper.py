import re
import requests
from bs4 import BeautifulSoup
from typing import Tuple, List, Dict
import spacy

# Load spaCy small NER model once
try:
    nlp = spacy.load("en_core_web_sm")
except:
    # if not installed, users will install:
    # python -m spacy download en_core_web_sm
    nlp = None

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
}
WIKI_MAIN_SELECTOR = "#mw-content-text"


def _clean_text(text: str) -> str:
    text = re.sub(r"\[\d+\]", "", text)  # remove citation refs like [1], [2]
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _extract_summary(paragraphs: List[str]) -> str:
    summary = []
    for p in paragraphs:
        if len(summary) >= 3:  # take first 3 meaningful paragraphs
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
    if not nlp:  # If spaCy isn't installed
        return {"people": [], "organizations": [], "locations": []}

    doc = nlp(text)
    people = sorted({ent.text for ent in doc.ents if ent.label_ == "PERSON"})
    orgs = sorted({ent.text for ent in doc.ents if ent.label_ == "ORG"})
    locs = sorted({ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]})

    return {
        "people": people[:15],
        "organizations": orgs[:15],
        "locations": locs[:15],
    }


def scrape_wikipedia(url: str) -> Tuple[str, str, List[str], Dict[str, List[str]], str]:
    """
    Returns:
      title,
      summary,
      sections,
      key_entities,
      full_cleaned_text
    """
    if not (url.startswith("http://") or url.startswith("https://")):
        raise ValueError("URL must start with http:// or https://")

    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Title
    title_tag = soup.find("h1", id="firstHeading")
    title = title_tag.get_text(strip=True) if title_tag else soup.title.get_text(strip=True)

    content_root = soup.select_one(WIKI_MAIN_SELECTOR)
    if not content_root:
        raise RuntimeError("Could not locate Wikipedia main content")

    # Remove unnecessary tags
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
