from __future__ import annotations

from typing import List, Optional
from bs4 import BeautifulSoup

from src.guidelines.models import GuidelineDocument, GuidelineSection, Evidence
from src.utils.dates import parse_date
from src.utils.evidence import extract_evidence


def parse_html(path: str, source: Optional[str] = None) -> GuidelineDocument:
    with open(path, "rb") as f:
        data = f.read()
    soup = BeautifulSoup(data, "lxml")

    title = _get_title(soup)
    pub, updated = _get_dates(soup)

    sections = _extract_sections(soup)

    raw_text_chars = len(soup.get_text("\n")) if soup else None

    return GuidelineDocument(
        id=None,
        title=title,
        source=source,
        url=None,
        publication_date=pub,
        last_updated=updated,
        sections=sections,
        raw_text_chars=raw_text_chars,
    )


def _get_title(soup: BeautifulSoup) -> Optional[str]:
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    h1 = soup.find(["h1", "h2"]) if soup else None
    if h1 and h1.get_text(strip=True):
        return h1.get_text(strip=True)
    return None


def _get_dates(soup: BeautifulSoup) -> tuple[Optional[str], Optional[str]]:
    pub = None
    updated = None
    for tag in soup.find_all(["time", "meta", "span", "p"]):
        text = tag.get("datetime") or tag.get("content") or tag.get_text(" ", strip=True)
        if not text:
            continue
        d = parse_date(text)
        if d:
            if tag.name == "time" and tag.get("itemprop") in {"datePublished", "dateCreated"}:
                pub = pub or d
            elif tag.name == "time" and tag.get("itemprop") in {"dateModified", "dateUpdated"}:
                updated = updated or d
            else:
                pub = pub or d
    return pub, updated


def _extract_sections(soup: BeautifulSoup) -> List[GuidelineSection]:
    sections: List[GuidelineSection] = []
    headers = soup.find_all(["h1", "h2", "h3", "h4"]) if soup else []

    for h in headers:
        heading = h.get_text(" ", strip=True)
        level = _level_from_tag(h.name)
        texts: List[str] = []
        # Gather following siblings until next header of same or higher level
        for sib in h.next_siblings:
            if getattr(sib, "name", None) in ["h1", "h2", "h3", "h4"]:
                break
            txt = sib.get_text("\n", strip=True) if hasattr(sib, "get_text") else str(sib).strip()
            if txt:
                texts.append(txt)
        body = "\n".join(texts).strip()

        sec = GuidelineSection(heading=heading, level=level, text=body)
        grade, system, notes = extract_evidence(body)
        if grade or system or notes:
            sec.evidence = Evidence(grade=grade, system=system, notes=notes)
        sections.append(sec)

    if not sections:
        # Fallback: whole page as one section
        body = soup.get_text("\n", strip=True)
        grade, system, notes = extract_evidence(body)
        sec = GuidelineSection(heading=None, level=1, text=body)
        if grade or system or notes:
            sec.evidence = Evidence(grade=grade, system=system, notes=notes)
        sections.append(sec)
    return sections


def _level_from_tag(tag: str) -> int:
    try:
        return int(tag[1]) if tag.startswith("h") and tag[1].isdigit() else 1
    except Exception:
        return 1
