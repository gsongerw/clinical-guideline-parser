from __future__ import annotations

from typing import Optional

from dateutil import parser as date_parser  # type: ignore[import-untyped]


def parse_date(text: str) -> Optional[str]:
    if not text:
        return None

    # Skip obviously non-date strings
    if len(text) < 4 or len(text) > 50:
        return None

    # Skip strings that don't contain any digits
    if not any(c.isdigit() for c in text):
        return None

    # Skip strings that are clearly not dates
    if any(
        word in text.lower()
        for word in ["width", "height", "scale", "device", "viewport", "charset"]
    ):
        return None

    try:
        dt = date_parser.parse(text, fuzzy=True, default=None)
        if dt:
            # Additional validation: check if the parsed date is reasonable
            year = dt.year
            if year < 1900 or year > 2030:
                return None
            return str(dt.date().isoformat())
    except Exception:
        return None
    return None
