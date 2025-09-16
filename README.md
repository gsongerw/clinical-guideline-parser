# Clinical Guideline Parser

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://github.com/yourusername/clinical-guideline-parser/workflows/Tests/badge.svg)](https://github.com/yourusername/clinical-guideline-parser/actions)

> **Transform medical guidelines into searchable, structured data for AI-powered clinical decision support**

A focused pipeline to parse medical guidelines (PDF/HTML) into structured JSON for downstream clinical RAG or summarization. This implements models, parsers, normalization utils, and a CLI to ingest documents into JSONL.

## 🚀 Features

- **📄 Multi-format Support**: Parse PDF via PyMuPDF and HTML via BeautifulSoup
- **🔍 Smart Search**: BM25-based search over section text with relevance scoring
- **📊 Evidence Extraction**: Automatically extract and normalize evidence grades (Class I, Level A, etc.)
- **📅 Date Intelligence**: Extract publication and update dates from documents
- **⚡ Fast Processing**: Batch processing with progress bars and error handling
- **🔧 CLI Tools**: Easy-to-use command-line interface for ingestion and search
- **📦 Structured Output**: JSONL format for easy integration with other systems

## 🏥 Why This Matters

- **Time Savings**: Reduce guideline lookup time from 5-10 minutes to 10-30 seconds
- **Cost Reduction**: Free alternative to expensive subscription services ($38-62/month)
- **Better Care**: Faster access to current, evidence-based recommendations
- **Scalability**: Process hundreds of guidelines automatically

## 📦 Installation

### From Source
```bash
git clone https://github.com/yourusername/clinical-guideline-parser.git
cd clinical-guideline-parser
pip install -e .
```

### Development Installation
```bash
git clone https://github.com/yourusername/clinical-guideline-parser.git
cd clinical-guideline-parser
pip install -e .[dev]
```

## 🚀 Quick Start

### 1. Parse Guidelines
```bash
# Process a folder of PDF/HTML files
clinical-ingest --input /path/to/guidelines --output /path/to/out --source "AHA/ACC"
```

### 2. Search Content
```bash
# Search through parsed guidelines
clinical-search --jsonl /path/to/out/guidelines.jsonl --query "heart failure ACE inhibitors" --k 5
```

### 3. Try the Demo
```bash
# Run the interactive demo
python examples/demo.py
```

## 📋 Example Output

```json
{
  "id": "aha-2023-hf",
  "title": "2023 AHA Guideline for Heart Failure",
  "source": "AHA/ACC",
  "publication_date": "2023-05-10",
  "last_updated": "2024-01-20",
  "sections": [
    {
      "heading": "Initial Evaluation",
      "level": 2,
      "text": "All patients with suspected heart failure should undergo comprehensive evaluation...",
      "evidence": {"grade": "A", "system": "AHA/ACC", "notes": "Class I, Level A"}
    }
  ]
}
```

## 🔍 Search Results

```json
{
  "results": [
    {
      "score": 0.85,
      "doc_id": "aha-2023-hf",
      "title": "2023 AHA Guideline for Heart Failure",
      "source": "AHA/ACC",
      "section_heading": "Pharmacological Management",
      "snippet": "ACE inhibitors are recommended for all patients with reduced ejection fraction...",
      "publication_date": "2023-05-10"
    }
  ]
}
```

## 🛠️ Advanced Usage

### Custom Evidence Grading
```python
from src.utils.evidence import extract_evidence

grade, system, notes = extract_evidence("Class I, Level A: This is recommended")
print(f"Grade: {grade}, System: {system}, Notes: {notes}")
```

### Batch Processing
```python
from src.parsers.pdf_parser import parse_pdf
from pathlib import Path

for pdf_file in Path("guidelines").glob("*.pdf"):
    doc = parse_pdf(str(pdf_file), source="Custom Source")
    print(f"Parsed {doc.title} with {doc.total_sections()} sections")
```

## 📚 Documentation

- **[Getting Started Guide](HOW_TO_RUN.txt)** - Step-by-step instructions for beginners
- **[Purpose & Value](purpose.txt)** - Detailed explanation of clinical implications
- **[API Reference](docs/api.md)** - Complete API documentation
- **[Examples](examples/)** - Sample code and demo scripts

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_parsers.py -v
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Important Notes

- **Not for Clinical Use**: This is a research/development tool, not a medical device
- **No PHI Handling**: Designed for public guideline documents only
- **Verify Sources**: Always verify information with official medical sources
- **Evidence Grades**: Heuristic extraction may need validation for clinical use

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/clinical-guideline-parser/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/clinical-guideline-parser/discussions)
- **Email**: your.email@example.com

## 🙏 Acknowledgments

- Built with [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF processing
- Search powered by [rank-bm25](https://github.com/dorianbrown/rank_bm25)
- Structured with [Pydantic](https://pydantic.dev/) for data validation
