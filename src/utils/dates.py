from __future__ import annotations

from typing import Optional
from dateutil import parser as date_parser


def parse_date(text: str) -> Optional[str]:
    if not text:
        return None
    try:
        dt = date_parser.parse(text, fuzzy=True, default=None)
        if dt:
            return dt.date().isoformat()
    except Exception:
        return None
    return None
