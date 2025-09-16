# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of clinical guideline parser
- PDF parsing with PyMuPDF
- HTML parsing with BeautifulSoup
- BM25 search functionality
- Evidence grade normalization
- Date extraction and normalization
- Command-line interface for ingestion and search
- Comprehensive documentation and examples

### Features
- Parse medical guidelines from PDF and HTML sources
- Extract structured data including sections, headings, dates, and evidence grades
- Fast BM25-based search over parsed content
- Support for multiple guideline sources (AHA/ACC, etc.)
- JSONL output format for easy integration
- Command-line tools for batch processing and querying

## [0.1.0] - 2024-01-XX

### Added
- Initial MVP implementation
- Basic PDF and HTML parsing
- BM25 search index
- Evidence grade extraction
- Date parsing and normalization
- CLI tools for ingestion and search
