# Contributing to Clinical Guideline Parser

Thank you for your interest in contributing to the Clinical Guideline Parser! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic understanding of medical guidelines and text processing

### Development Setup
1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/clinical-guideline-parser.git
   cd clinical-guideline-parser
   ```
3. Install in development mode:
   ```bash
   pip install -e .[dev]
   ```
4. Run tests to ensure everything works:
   ```bash
   pytest
   ```

## 🛠️ Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes
- Write code following the existing style
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 3. Code Style
We use several tools to maintain code quality:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run these before committing:
```bash
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/
```

### 4. Testing
- Write tests for new functionality
- Ensure existing tests still pass
- Aim for good test coverage

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_parsers.py -v
```

### 5. Commit and Push
```bash
git add .
git commit -m "Add: Brief description of changes"
git push origin feature/your-feature-name
```

### 6. Create a Pull Request
- Go to your fork on GitHub
- Click "New Pull Request"
- Fill out the PR template
- Request review from maintainers

## 📝 Types of Contributions

### Bug Reports
- Use the GitHub issue template
- Include steps to reproduce
- Provide error messages and system information

### Feature Requests
- Use the GitHub issue template
- Describe the use case and expected behavior
- Consider implementation complexity

### Code Contributions
- Bug fixes
- New parsers (e.g., for different document formats)
- Improved evidence extraction
- Enhanced search functionality
- Performance improvements
- Documentation improvements

## 🧪 Testing Guidelines

### Test Structure
- Unit tests for individual functions
- Integration tests for parsers
- End-to-end tests for CLI tools

### Test Data
- Use the sample files in `examples/`
- Create minimal test cases
- Avoid including large PDF files in the repository

### Example Test
```python
def test_evidence_extraction():
    from src.utils.evidence import extract_evidence
    
    grade, system, notes = extract_evidence("Class I, Level A: Recommended")
    assert grade == "A"
    assert system is not None
    assert "Class I" in notes
```

## 📚 Documentation

### Code Documentation
- Use docstrings for all public functions
- Follow Google docstring format
- Include type hints

### User Documentation
- Update README.md for user-facing changes
- Add examples for new features
- Update HOW_TO_RUN.txt for workflow changes

### API Documentation
- Document new public APIs
- Include usage examples
- Update type hints

## 🏥 Medical Guidelines Considerations

### Content Guidelines
- Only process publicly available guidelines
- Respect copyright and licensing
- Don't include patient data or PHI
- Verify information accuracy

### Evidence Grades
- Follow standard medical evidence grading systems
- AHA/ACC, GRADE, etc.
- Document any custom grading schemes

### Clinical Safety
- This tool is for research/development only
- Not approved for clinical use
- Always verify with official sources

## 🔍 Code Review Process

### What We Look For
- Code quality and style
- Test coverage
- Documentation completeness
- Performance considerations
- Security implications
- Medical accuracy

### Review Checklist
- [ ] Code follows project style guidelines
- [ ] Tests are included and pass
- [ ] Documentation is updated
- [ ] No breaking changes without discussion
- [ ] Performance impact is considered
- [ ] Security implications are addressed

## 🐛 Reporting Issues

### Before Reporting
1. Check existing issues
2. Try the latest version
3. Test with sample data

### Issue Template
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. See error

**Expected behavior**
What you expected to happen.

**Environment**
- OS: [e.g., macOS, Linux, Windows]
- Python version: [e.g., 3.9.0]
- Package version: [e.g., 0.1.0]

**Additional context**
Any other relevant information.
```

## 💡 Ideas for Contributions

### Parser Improvements
- Support for more document formats (Word, RTF, etc.)
- Better table extraction
- Image and diagram processing
- Multi-language support

### Search Enhancements
- Semantic search with embeddings
- Faceted search (by source, date, specialty)
- Query expansion
- Result ranking improvements

### Clinical Features
- Specialty-specific parsing rules
- Risk calculator integration
- Drug interaction checking
- Outcome prediction

### Infrastructure
- Docker containerization
- Web API interface
- Database integration
- Caching layer

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and ideas
- **Email**: your.email@example.com

## 🙏 Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- GitHub contributor list

Thank you for contributing to improving healthcare through better access to medical guidelines!
