from __future__ import annotations

import re
from typing import Optional, Tuple

CLASS_PATTERN = re.compile(r"\bClass\s+(I{1,3}|IIa|IIb|III)\b", re.IGNORECASE)
LEVEL_PATTERN = re.compile(r"\b(Level|Evidence)\s+(A|B|C)\b", re.IGNORECASE)


def extract_evidence(text: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    if not text:
        return None, None, None
    cls = None
    lvl = None

    cls_m = CLASS_PATTERN.search(text)
    if cls_m:
        cls = cls_m.group(1)  # Keep original case for Roman numerals

    lvl_m = LEVEL_PATTERN.search(text)
    if lvl_m:
        lvl = lvl_m.group(2).upper()  # Uppercase for A, B, C

    # Canonical grade preference: Level first if present, else Class
    canonical = lvl or cls

    system = None
    if cls or lvl:
        system = "AHA/ACC or GRADE (heuristic)"

    notes = None
    if cls and lvl:
        notes = f"Class {cls}, Level {lvl}"

    return canonical, system, notes
