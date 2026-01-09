from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional

import requests
from bs4 import BeautifulSoup


DEFAULT_TAGS = ["h1", "h2", "h3", "h4", "h5", "h6", "p"]


@dataclass
class ScrapeResult:
    url: str
    title: str
    blocks: List[str]
    text: str


def normalize_whitespace(s: str) -> str:
    s = s.replace("\u00a0", " ")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def fetch_html(url: str, timeout: int = 20) -> str:
    headers = {"User-Agent": "NMR-Scraper/1.0 (educational project)"}
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    if not resp.encoding:
        resp.encoding = resp.apparent_encoding
    return resp.text


def extract_text(html: str, tags: Optional[List[str]] = None) -> tuple[str, List[str], str]:
    tags = tags or DEFAULT_TAGS
    soup = BeautifulSoup(html, "lxml")

    for t in soup(["script", "style", "noscript"]):
        t.decompose()

    title = soup.title.get_text(strip=True) if soup.title else ""

    blocks: List[str] = []
    for el in soup.find_all(tags):
        txt = el.get_text(separator=" ", strip=True)
        if txt:
            blocks.append(txt)

    text = normalize_whitespace("\n".join(blocks))
    return title, blocks, text


def scrape_url(url: str, tags: Optional[List[str]] = None) -> ScrapeResult:
    if not (url.startswith("http://") or url.startswith("https://")):
        raise ValueError("URL mora početi s http:// ili https://")

    html = fetch_html(url)
    title, blocks, text = extract_text(html, tags=tags)
    return ScrapeResult(url=url, title=title, blocks=blocks, text=text)
