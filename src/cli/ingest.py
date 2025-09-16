from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Iterable, Optional

from rich.progress import track

from src.parsers.html_parser import parse_html
from src.parsers.pdf_parser import parse_pdf


def find_files(input_dir: str) -> Iterable[Path]:
    p = Path(input_dir)
    for ext in ("*.pdf", "*.PDF", "*.html", "*.htm", "*.HTML", "*.HTM"):
        for f in p.rglob(ext):
            if f.is_file():
                yield f


def parse_file(path: Path, source: Optional[str] = None):
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return parse_pdf(str(path), source=source)
    elif suffix in {".html", ".htm"}:
        return parse_html(str(path), source=source)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")


def main():
    parser = argparse.ArgumentParser(
        description="Ingest clinical guidelines into structured JSONL"
    )
    parser.add_argument(
        "--input", required=True, help="Input directory containing guideline files"
    )
    parser.add_argument("--output", required=True, help="Output directory for JSONL")
    parser.add_argument(
        "--format", default="jsonl", choices=["jsonl"], help="Output format"
    )
    parser.add_argument("--source", default=None, help="Source label, e.g., AHA/ACC")

    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    out_path = Path(args.output) / "guidelines.jsonl"

    count = 0
    with open(out_path, "w", encoding="utf-8") as out:
        for f in track(list(find_files(args.input)), description="Parsing guidelines"):
            try:
                doc = parse_file(f, source=args.source)
                record = doc.model_dump()
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                count += 1
            except Exception as e:
                # Log to stderr but continue
                print(f"Failed to parse {f}: {e}")

    print(f"Wrote {count} records to {out_path}")


if __name__ == "__main__":
    main()
