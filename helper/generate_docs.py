#!/usr/bin/env python3
"""
Generate HTML documentation from Markdown sources.

This script converts Markdown documentation to HTML with:
- Light and dark mode CSS
- Syntax highlighting for code blocks
- Table of contents
- Responsive design
"""

import markdown
from pathlib import Path
import sys

# CSS for light/dark mode with syntax highlighting
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - AI Provenance</title>
    <style>
        :root {{
            --bg: #ffffff;
            --text: #24292e;
            --code-bg: #f6f8fa;
            --border: #e1e4e8;
            --link: #0366d6;
            --heading: #24292e;
        }}

        @media (prefers-color-scheme: dark) {{
            :root {{
                --bg: #0d1117;
                --text: #c9d1d9;
                --code-bg: #161b22;
                --border: #30363d;
                --link: #58a6ff;
                --heading: #c9d1d9;
            }}
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: var(--text);
            background: var(--bg);
            padding: 2rem;
            max-width: 900px;
            margin: 0 auto;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: var(--heading);
            margin: 1.5rem 0 1rem;
            font-weight: 600;
        }}

        h1 {{
            font-size: 2rem;
            border-bottom: 1px solid var(--border);
            padding-bottom: 0.3rem;
        }}

        h2 {{
            font-size: 1.5rem;
            border-bottom: 1px solid var(--border);
            padding-bottom: 0.3rem;
        }}

        h3 {{ font-size: 1.25rem; }}

        p {{
            margin: 1rem 0;
        }}

        code {{
            background: var(--code-bg);
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 85%;
        }}

        pre {{
            background: var(--code-bg);
            padding: 1rem;
            border-radius: 6px;
            overflow-x: auto;
            margin: 1rem 0;
        }}

        pre code {{
            background: none;
            padding: 0;
        }}

        a {{
            color: var(--link);
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        ul, ol {{
            margin: 1rem 0;
            padding-left: 2rem;
        }}

        li {{
            margin: 0.5rem 0;
        }}

        blockquote {{
            border-left: 4px solid var(--border);
            padding-left: 1rem;
            margin: 1rem 0;
            color: var(--text);
            opacity: 0.8;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1rem 0;
        }}

        th, td {{
            border: 1px solid var(--border);
            padding: 0.5rem;
            text-align: left;
        }}

        th {{
            background: var(--code-bg);
            font-weight: 600;
        }}

        .toc {{
            background: var(--code-bg);
            border: 1px solid var(--border);
            padding: 1rem;
            border-radius: 6px;
            margin: 2rem 0;
        }}

        .toc-title {{
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}

        hr {{
            border: none;
            border-top: 1px solid var(--border);
            margin: 2rem 0;
        }}
    </style>
</head>
<body>
    <nav style="margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border);">
        <a href="index.html">Home</a> |
        <a href="user-guide.html">User Guide</a> |
        <a href="../api/index.html">API Docs</a>
    </nav>
    {content}
    <footer style="margin-top: 4rem; padding-top: 2rem; border-top: 1px solid var(--border); text-align: center; opacity: 0.7;">
        <p>Generated with AI Provenance Documentation Generator</p>
    </footer>
</body>
</html>
'''


def generate_html(md_file: Path, output_file: Path, title: str = None):
    """Generate HTML from Markdown file."""
    if not md_file.exists():
        print(f"Error: {md_file} not found")
        return False

    # Read markdown
    md_content = md_file.read_text()

    # Convert to HTML with extensions
    html_content = markdown.markdown(
        md_content,
        extensions=[
            'toc',
            'tables',
            'fenced_code',
            'codehilite',
            'nl2br',
            'sane_lists'
        ]
    )

    # Use filename as title if not provided
    if title is None:
        title = md_file.stem.replace('-', ' ').replace('_', ' ').title()

    # Wrap in template
    full_html = HTML_TEMPLATE.format(
        title=title,
        content=html_content
    )

    # Write output
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(full_html)
    print(f"✓ Generated {output_file}")
    return True


def main():
    """Generate all documentation HTML files."""
    repo_root = Path(__file__).parent.parent

    docs_to_generate = [
        # (source_md, output_html, title)
        (repo_root / "README.md", repo_root / "docs" / "guides" / "user-guide.html", "User Guide"),
        (repo_root / "docs" / "REQUIREMENTS_WORKFLOW.md", repo_root / "docs" / "guides" / "requirements-workflow.html", "Requirements Workflow"),
    ]

    success_count = 0
    for md_file, html_file, title in docs_to_generate:
        if generate_html(md_file, html_file, title):
            success_count += 1

    print(f"\n✓ Generated {success_count}/{len(docs_to_generate)} documentation files")

    # Generate index
    index_html = repo_root / "docs" / "guides" / "index.html"
    index_content = markdown.markdown("""
# AI Provenance Documentation

## Guides

- [User Guide](user-guide.html) - Complete guide to using ai-provenance
- [Requirements Workflow](requirements-workflow.html) - Managing requirements with ai-provenance

## API Documentation

- [API Reference](../api/index.html) - Python API documentation

## Resources

- [GitHub Repository](https://github.com/ai-provenance/ai-provenance)
- [PyPI Package](https://pypi.org/project/ai-provenance/)
""")
    generate_html(
        repo_root / "README.md",  # Dummy, we're using custom content
        index_html,
        "Documentation Index"
    )
    # Override with custom index
    full_html = HTML_TEMPLATE.format(
        title="Documentation Index",
        content=index_content
    )
    index_html.write_text(full_html)
    print(f"✓ Generated {index_html}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
