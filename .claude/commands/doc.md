# Generate and Manage Documentation

You are helping the user with documentation tasks for ai-provenance.

**Use the AskUserQuestion tool to ask what documentation task they need:**

## Available Documentation Tasks

### 1. Generate User Guide HTML
Generate HTML versions of user guides from Markdown sources.

**Actions:**
- Convert README.md to HTML (light and dark mode)
- Generate docs/guides/user-guide.html
- Include CSS for professional styling
- Add navigation and table of contents
- Save to docs/guides/ directory

**Command:**
```bash
# Using Python markdown library
python helper/generate_docs.py
```

### 2. Update README.md
Comprehensively update the main README with latest features.

**Include:**
- Feature list (from CLAUDE.md)
- Installation instructions
- Quick start guide
- CLI command reference
- Examples
- Slash command documentation (/req, /implement, etc.)

### 3. Generate API Documentation
Create API docs from docstrings.

**Actions:**
- Run pdoc or sphinx to extract docstrings
- Generate docs/api/index.html
- Document all CLI commands
- Document all Python modules

### 4. Update CLAUDE.md
Update project context file with:
- Recent session updates
- New features added
- Updated technical limitations
- New commands and capabilities

### 5. Generate Changelog
Create or update CHANGELOG.md from git commits.

**Actions:**
- Extract commits since last release
- Group by type (feat, fix, docs, etc.)
- Format as Keep a Changelog format
- Include AI provenance statistics

### 6. Create Tutorial/Guide
Generate step-by-step tutorials:
- Getting Started Guide
- Requirements Workflow Guide
- Traceability Best Practices
- CI/CD Integration Guide

## Workflow

1. Ask user which documentation task
2. For HTML generation:
   - Check if helper/generate_docs.py exists
   - If not, create it with markdown → HTML conversion
   - Include CSS for light/dark modes
   - Generate and save HTML files
3. For README updates:
   - Read current README.md
   - Read CLAUDE.md for latest features
   - Update README with comprehensive info
   - Preserve existing examples
4. Show user what was generated
5. Ask if they want to commit the changes

## HTML Generation Details

Use Python's markdown library:
```python
import markdown
from pathlib import Path

# Convert with extensions
html = markdown.markdown(
    md_content,
    extensions=['toc', 'tables', 'fenced_code', 'codehilite']
)

# Wrap in HTML template with CSS
template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>
        /* Light and dark mode CSS */
        @media (prefers-color-scheme: dark) {{ ... }}
    </style>
</head>
<body>
    {content}
</body>
</html>
'''
```

## Pre-commit Hook Integration

Suggest adding to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# Regenerate docs before commit
python helper/generate_docs.py
git add docs/guides/*.html
```

Be helpful and guide the user through the documentation process!
