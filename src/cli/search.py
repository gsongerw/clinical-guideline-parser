from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.search.bm25_index import BM25SectionIndex


def main():
    parser = argparse.ArgumentParser(description="Search guideline JSONL with BM25")
    parser.add_argument("--jsonl", required=True, help="Path to guidelines.jsonl")
    parser.add_argument("--query", required=True, help="Search query text")
    parser.add_argument("--k", type=int, default=5, help="Top-k results")
    args = parser.parse_args()

    if not Path(args.jsonl).exists():
        raise SystemExit(f"JSONL not found: {args.jsonl}")

    index = BM25SectionIndex.from_jsonl(args.jsonl)
    results = index.search(args.query, k=args.k)

    print(json.dumps({"results": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
