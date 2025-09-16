#!/bin/bash

# GitHub Setup Script for Clinical Guideline Parser
# This script helps you set up the repository for GitHub

echo "🏥 Setting up Clinical Guideline Parser for GitHub"
echo "=================================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Add all files to git
echo "📁 Adding files to Git..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Clinical Guideline Parser MVP

- PDF and HTML parsing with PyMuPDF and BeautifulSoup
- BM25 search functionality
- Evidence grade extraction and normalization
- Date parsing and normalization
- CLI tools for ingestion and search
- Comprehensive documentation and examples
- Test suite and CI/CD setup"

echo "✅ Initial commit created"

# Create main branch if it doesn't exist
if [ "$(git branch --show-current)" != "main" ]; then
    echo "🌿 Creating main branch..."
    git branch -M main
fi

echo ""
echo "🚀 Next steps to publish to GitHub:"
echo "1. Create a new repository on GitHub (https://github.com/new)"
echo "2. Copy the repository URL"
echo "3. Run these commands:"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/clinical-guideline-parser.git"
echo "   git push -u origin main"
echo ""
echo "4. Update the URLs in README.md and pyproject.toml with your actual GitHub username"
echo ""
echo "📝 Don't forget to:"
echo "   - Update your email in pyproject.toml"
echo "   - Replace 'yourusername' in README.md with your GitHub username"
echo "   - Add a description and topics to your GitHub repository"
echo "   - Enable GitHub Actions for CI/CD"
echo ""
echo "✅ Setup complete! Your project is ready for GitHub."
