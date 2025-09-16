#!/usr/bin/env python3
"""
Demo script showing how to use the clinical guideline parser.
This script demonstrates parsing and searching sample guidelines.
"""

import json
import os
import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.parsers.html_parser import parse_html
from src.search.bm25_index import BM25SectionIndex


def main():
    print("🏥 Clinical Guideline Parser Demo")
    print("=" * 50)
    
    # Get the example file path
    example_file = Path(__file__).parent / "sample_guideline.html"
    
    if not example_file.exists():
        print(f"❌ Example file not found: {example_file}")
        return
    
    print(f"📄 Parsing example guideline: {example_file.name}")
    
    # Parse the HTML file
    try:
        doc = parse_html(str(example_file), source="AHA/ACC")
        print(f"✅ Successfully parsed document:")
        print(f"   Title: {doc.title}")
        print(f"   Source: {doc.source}")
        print(f"   Publication Date: {doc.publication_date}")
        print(f"   Last Updated: {doc.last_updated}")
        print(f"   Number of Sections: {doc.total_sections()}")
        print()
        
        # Show sections with evidence grades
        print("📋 Document Sections:")
        for i, section in enumerate(doc.sections, 1):
            print(f"   {i}. {section.heading or 'No heading'}")
            if section.evidence and section.evidence.grade:
                print(f"      Evidence: {section.evidence.grade} ({section.evidence.system})")
            print(f"      Text preview: {section.text[:100]}...")
            print()
        
        # Create search index
        print("🔍 Creating search index...")
        sections = []
        for section in doc.sections:
            if section.text.strip():
                sections.append({
                    "doc_id": doc.id or "sample-doc",
                    "title": doc.title,
                    "source": doc.source,
                    "section_heading": section.heading,
                    "section_level": section.level,
                    "publication_date": doc.publication_date,
                    "last_updated": doc.last_updated,
                    "text": section.text,
                })
        
        # Create a temporary JSONL file for the search index
        temp_jsonl = Path(__file__).parent / "temp_guidelines.jsonl"
        with open(temp_jsonl, "w", encoding="utf-8") as f:
            f.write(json.dumps({
                "id": doc.id or "sample-doc",
                "title": doc.title,
                "source": doc.source,
                "url": None,
                "publication_date": doc.publication_date,
                "last_updated": doc.last_updated,
                "sections": [{"heading": s["section_heading"], "level": s["section_level"], "text": s["text"]} for s in sections]
            }) + "\n")
        
        # Create search index
        index = BM25SectionIndex.from_jsonl(str(temp_jsonl))
        
        # Demo searches
        demo_queries = [
            "ACE inhibitors heart failure",
            "beta blockers mortality",
            "device therapy ICD",
            "lifestyle modifications exercise"
        ]
        
        print("🔍 Demo Searches:")
        print("-" * 30)
        
        for query in demo_queries:
            print(f"\nQuery: '{query}'")
            results = index.search(query, k=2)
            
            if results:
                for i, result in enumerate(results, 1):
                    print(f"  {i}. Score: {result['score']:.3f}")
                    print(f"     Section: {result['section_heading']}")
                    print(f"     Snippet: {result['snippet'][:150]}...")
            else:
                print("  No results found")
        
        # Clean up
        temp_jsonl.unlink()
        
        print(f"\n✅ Demo completed successfully!")
        print(f"   Parsed {doc.total_sections()} sections")
        print(f"   Found evidence grades in {sum(1 for s in doc.sections if s.evidence and s.evidence.grade)} sections")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
