from __future__ import annotations

import re
from typing import List, Optional

import fitz  # PyMuPDF

from src.guidelines.models import Evidence, GuidelineDocument, GuidelineSection
from src.utils.dates import parse_date
from src.utils.evidence import extract_evidence

HEADING_LINE = re.compile(r"^(\d+\.|[A-Z][A-Z\s\-/]{3,}|[IVX]+\.)\s+.*")
DATE_CANDIDATE = re.compile(
    r"(Published|Publication|Updated|Last\s+updated|Revision)[:\s]+(.{4,60})",
    re.IGNORECASE,
)
TITLE_CANDIDATE = re.compile(
    r"^(.*Guideline.*|.*Statement.*|.*Recommendation.*)$", re.IGNORECASE
)


def parse_pdf(path: str, source: Optional[str] = None) -> GuidelineDocument:
    doc = fitz.open(path)
    full_text_lines: List[str] = []
    for page in doc:
        text = page.get_text("text")
        if text:
            full_text_lines.extend([line.rstrip() for line in text.splitlines()])
    raw_text = "\n".join(full_text_lines)

    title = _infer_title(full_text_lines)
    pub_date, last_updated = _infer_dates(full_text_lines)

    sections = _split_into_sections(full_text_lines)

    gl = GuidelineDocument(
        id=None,
        title=title,
        source=source,
        url=None,
        publication_date=pub_date,
        last_updated=last_updated,
        sections=sections,
        raw_text_chars=len(raw_text),
    )
    return gl


def _infer_title(lines: List[str]) -> Optional[str]:
    # First non-empty line matching title heuristic
    for line in lines[:60]:
        s = line.strip()
        if not s:
            continue
        if TITLE_CANDIDATE.match(s):
            return s
    # fallback: first strong-looking line
    for line in lines[:20]:
        s = line.strip()
        if s:
            return s
    return None


def _infer_dates(lines: List[str]) -> tuple[Optional[str], Optional[str]]:
    pub = None
    updated = None
    for line in lines[:200]:
        m = DATE_CANDIDATE.search(line)
        if m:
            candidate = parse_date(m.group(2))
            if candidate:
                key = m.group(1).lower()
                if "update" in key or "revision" in key:
                    updated = updated or candidate
                else:
                    pub = pub or candidate
    # generic scan as fallback
    if not pub:
        for line in lines[:150]:
            d = parse_date(line)
            if d:
                pub = d
                break
    return pub, updated


def _split_into_sections(lines: List[str]) -> List[GuidelineSection]:
    sections: List[GuidelineSection] = []
    current: Optional[GuidelineSection] = None

    def flush():
        nonlocal current
        if current is not None:
            current.text = current.text.strip()
            if current.text:
                sections.append(current)
            current = None

    for line in lines:
        s = line.strip()
        if not s:
            continue
        if HEADING_LINE.match(s):
            flush()
            current = GuidelineSection(heading=s, level=_heading_level(s), text="")
        else:
            if current is None:
                current = GuidelineSection(heading=None, level=1, text="")
            current.text += s + "\n"

    flush()

    # Evidence extraction pass
    for sec in sections:
        grade, system, notes = extract_evidence(sec.text)
        if grade or system or notes:
            sec.evidence = Evidence(grade=grade, system=system, notes=notes)

    return sections


def _heading_level(text: str) -> int:
    # Simple heuristic: numbered headings => deeper levels
    if re.match(r"^\d+\.\d+", text):
        return 3
    if re.match(r"^\d+\.\s", text):
        return 2
    if re.match(r"^[IVX]+\.\s", text):
        return 2
    # ALL CAPS looks like top-level
    if text.isupper():
        return 1
    return 2
