from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Optional

from rank_bm25 import BM25Okapi

TOKEN = re.compile(r"\b[\w\-]+\b", re.UNICODE)


def tokenize(text: str) -> List[str]:
    return [t.lower() for t in TOKEN.findall(text or "")]


@dataclass
class SectionRef:
    doc_id: str
    title: str | None
    source: str | None
    section_heading: str | None
    section_level: int
    publication_date: str | None
    last_updated: str | None
    text: str


class BM25SectionIndex:
    def __init__(self, sections: List[SectionRef]):
        self.sections = sections
        if not sections:
            self.bm25: Optional[BM25Okapi] = None
        else:
            corpus = [tokenize(s.text) for s in sections]
            self.bm25 = BM25Okapi(corpus)

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        if not self.sections or not self.bm25:
            return []
        tokens = tokenize(query)
        scores = self.bm25.get_scores(tokens)
        ranked = sorted(zip(self.sections, scores), key=lambda x: x[1], reverse=True)[
            :k
        ]
        results: List[Dict[str, Any]] = []
        for ref, score in ranked:
            results.append(
                {
                    "score": float(score),
                    "doc_id": ref.doc_id,
                    "title": ref.title,
                    "source": ref.source,
                    "section_heading": ref.section_heading,
                    "section_level": ref.section_level,
                    "publication_date": ref.publication_date,
                    "last_updated": ref.last_updated,
                    "snippet": ref.text[:800],
                }
            )
        return results

    @staticmethod
    def from_jsonl(path: str) -> "BM25SectionIndex":
        sections: List[SectionRef] = []
        content = Path(path).read_text(encoding="utf-8") if Path(path).exists() else ""
        for line in content.splitlines():
            if not line.strip():
                continue
            obj = json.loads(line)
            doc_id = obj.get("id") or ""
            title = obj.get("title")
            source = obj.get("source")
            pub = obj.get("publication_date")
            upd = obj.get("last_updated")
            for sec in obj.get("sections", []) or []:
                text = sec.get("text") or ""
                heading = sec.get("heading")
                level = int(sec.get("level") or 1)
                if not text.strip():
                    continue
                sections.append(
                    SectionRef(
                        doc_id=doc_id,
                        title=title,
                        source=source,
                        section_heading=heading,
                        section_level=level,
                        publication_date=pub,
                        last_updated=upd,
                        text=text,
                    )
                )
        return BM25SectionIndex(sections)
