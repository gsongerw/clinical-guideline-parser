from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    grade: Optional[str] = Field(
        default=None,
        description="Canonical evidence grade (e.g., A, B, C, I, IIa, IIb)",
    )
    system: Optional[str] = Field(
        default=None, description="Original grading system, e.g., AHA/ACC, GRADE"
    )
    notes: Optional[str] = None


class GuidelineSection(BaseModel):
    heading: Optional[str] = None
    level: int = 1
    text: str = ""
    evidence: Optional[Evidence] = None


class GuidelineDocument(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None

    publication_date: Optional[str] = Field(
        default=None, description="YYYY-MM-DD when available"
    )
    last_updated: Optional[str] = Field(
        default=None, description="YYYY-MM-DD when available"
    )

    sections: List[GuidelineSection] = Field(default_factory=list)

    raw_text_chars: Optional[int] = None

    def total_sections(self) -> int:
        return len(self.sections)
