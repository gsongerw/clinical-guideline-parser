"""Tests for the parsers module."""

import pytest
from pathlib import Path
from src.parsers.html_parser import parse_html
from src.parsers.pdf_parser import parse_pdf


class TestHTMLParser:
    """Test HTML parsing functionality."""
    
    def test_parse_sample_html(self):
        """Test parsing the sample HTML file."""
        sample_file = Path(__file__).parent.parent / "examples" / "sample_guideline.html"
        
        if not sample_file.exists():
            pytest.skip("Sample HTML file not found")
        
        doc = parse_html(str(sample_file), source="AHA/ACC")
        
        assert doc.title == "2023 AHA/ACC Heart Failure Management Guidelines"
        assert doc.source == "AHA/ACC"
        assert doc.publication_date == "2023-05-10"
        assert doc.last_updated == "2024-01-15"
        assert len(doc.sections) > 0
        
        # Check that we found evidence grades
        evidence_sections = [s for s in doc.sections if s.evidence and s.evidence.grade]
        assert len(evidence_sections) > 0
        
        # Check specific evidence grades
        ace_section = next((s for s in doc.sections if "ACE inhibitors" in s.text), None)
        assert ace_section is not None
        assert ace_section.evidence is not None
        assert ace_section.evidence.grade == "A"


class TestPDFParser:
    """Test PDF parsing functionality."""
    
    def test_parse_nonexistent_pdf(self):
        """Test that parsing a nonexistent PDF raises an appropriate error."""
        with pytest.raises(Exception):  # PyMuPDF raises FileNotFoundError
            parse_pdf("nonexistent.pdf")
    
    def test_parse_empty_pdf(self):
        """Test parsing behavior with empty input."""
        # This would need a test PDF file to be meaningful
        pytest.skip("No test PDF available")


class TestEvidenceExtraction:
    """Test evidence grade extraction."""
    
    def test_evidence_patterns(self):
        """Test that evidence patterns are correctly identified."""
        from src.utils.evidence import extract_evidence
        
        # Test Class I, Level A pattern
        grade, system, notes = extract_evidence("Class I, Level A: This is recommended")
        assert grade == "A"  # Level takes precedence
        assert system is not None
        assert "Class I" in notes
        
        # Test Level A pattern only
        grade, system, notes = extract_evidence("Level A evidence supports this")
        assert grade == "A"
        assert system is not None
        
        # Test Class IIa pattern only
        grade, system, notes = extract_evidence("Class IIa recommendation")
        assert grade == "IIa"
        assert system is not None


class TestDateExtraction:
    """Test date extraction functionality."""
    
    def test_date_parsing(self):
        """Test that dates are correctly parsed."""
        from src.utils.dates import parse_date
        
        # Test various date formats
        assert parse_date("2023-05-10") == "2023-05-10"
        assert parse_date("May 10, 2023") == "2023-05-10"
        assert parse_date("10/05/2023") == "2023-05-10"
        assert parse_date("invalid date") is None
        assert parse_date("") is None
