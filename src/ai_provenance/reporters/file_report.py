"""
File-level provenance reports.
"""

import json
from pathlib import Path
from typing import Optional

import git

from ai_provenance.core.models import FileMetadata
from ai_provenance.git_integration.notes import get_notes
from ai_provenance.parsers.stamper import parse_inline_metadata


def generate_file_report(
    file_path: str,
    revision: str = "HEAD",
    output_format: str = "text",
    repo_path: Optional[str] = None,
) -> str:
    """
    Generate a comprehensive metadata report for a file.

    Args:
        file_path: Path to the file (relative to repo root)
        revision: Git revision (default: HEAD)
        output_format: Output format (text, json, md)
        repo_path: Path to repository (default: current directory)

    Returns:
        Formatted report string
    """
    repo = git.Repo(repo_path or ".", search_parent_directories=True)
    repo_root = Path(repo.working_dir)
    full_path = repo_root / file_path

    # Get file content at revision
    try:
        file_content = repo.git.show(f"{revision}:{file_path}")
    except git.GitCommandError:
        raise FileNotFoundError(f"File not found at revision {revision}: {file_path}")

    # Parse .meta.json if exists
    metadata = None
    meta_path = f"{file_path}.meta.json"
    try:
        meta_content = repo.git.show(f"{revision}:{meta_path}")
        metadata = FileMetadata.model_validate_json(meta_content)
    except git.GitCommandError:
        # No .meta.json file
        pass

    # Get commit metadata from git notes
    commit = repo.commit(revision)
    commit_notes = get_notes(commit.hexsha, repo_path=repo_path)

    # Parse inline metadata
    # Save temp file to parse
    temp_file = repo_root / ".ai-prov-temp"
    temp_file.write_text(file_content)
    inline_metadata = parse_inline_metadata(str(temp_file))
    temp_file.unlink()

    # Build report
    if output_format == "json":
        return _format_json_report(file_path, metadata, commit_notes, inline_metadata)
    elif output_format == "md":
        return _format_markdown_report(file_path, revision, metadata, commit_notes, inline_metadata)
    else:
        return _format_text_report(file_path, revision, metadata, commit_notes, inline_metadata)


def _format_json_report(file_path, metadata, commit_notes, inline_metadata) -> str:
    """Format report as JSON."""
    report = {
        "file": file_path,
        "file_metadata": metadata.model_dump() if metadata else None,
        "commit_metadata": commit_notes,
        "inline_metadata": [
            {"line": line, "metadata": meta} for line, meta in inline_metadata
        ],
    }
    return json.dumps(report, indent=2)


def _format_markdown_report(file_path, revision, metadata, commit_notes, inline_metadata) -> str:
    """Format report as Markdown."""
    lines = [
        f"# AI Metadata Report: {file_path}",
        f"**Revision:** `{revision}`",
        "",
    ]

    # File-level metadata
    if metadata:
        lines.extend([
            "## File-Level Metadata",
            "",
            f"- **AI Tool:** {metadata.ai_tool.value if metadata.ai_tool else 'N/A'}",
            f"- **Confidence:** {metadata.confidence.value if metadata.confidence else 'N/A'}",
            f"- **Generated:** {metadata.generated_at}",
            f"- **Reviewed by:** {metadata.reviewed_by or 'Not reviewed'}",
        ])

        if metadata.trace:
            lines.append(f"- **Traces:** {', '.join(metadata.trace)}")
        if metadata.tests:
            lines.append(f"- **Tests:** {', '.join(metadata.tests)}")

        if metadata.blocks:
            lines.extend(["", "### Code Blocks", ""])
            for block in metadata.blocks:
                ai_marker = "🤖 AI" if block.ai else "👤 Human"
                lines.append(
                    f"- **{block.name}** ({block.kind.value}, lines {block.lines[0]}-{block.lines[1]}) {ai_marker}"
                )

        ai_pct = metadata.ai_percentage()
        lines.append(f"\n**AI-generated:** {ai_pct:.1f}%")

    # Commit metadata
    if commit_notes:
        lines.extend(["", "## Commit Metadata (Git Notes)", "", "```json"])
        lines.append(json.dumps(commit_notes, indent=2))
        lines.append("```")

    # Inline metadata
    if inline_metadata:
        lines.extend(["", "## Inline Metadata", ""])
        for line_num, meta in inline_metadata:
            lines.append(f"- **Line {line_num}:** `{json.dumps(meta)}`")

    return "\n".join(lines)


def _format_text_report(file_path, revision, metadata, commit_notes, inline_metadata) -> str:
    """Format report as plain text."""
    lines = [
        f"AI Metadata Report: {file_path} @ {revision}",
        "=" * 60,
        "",
    ]

    if metadata:
        lines.extend([
            "File-Level Metadata:",
            f"  AI Tool:     {metadata.ai_tool.value if metadata.ai_tool else 'N/A'}",
            f"  Confidence:  {metadata.confidence.value if metadata.confidence else 'N/A'}",
            f"  Generated:   {metadata.generated_at}",
            f"  Reviewed by: {metadata.reviewed_by or 'Not reviewed'}",
        ])

        if metadata.trace:
            lines.append(f"  Traces:      {', '.join(metadata.trace)}")
        if metadata.tests:
            lines.append(f"  Tests:       {', '.join(metadata.tests)}")

        ai_pct = metadata.ai_percentage()
        lines.append(f"  AI-generated: {ai_pct:.1f}%")
        lines.append("")

    if commit_notes:
        lines.extend(["Commit Metadata:", f"  {json.dumps(commit_notes, indent=2)}", ""])

    if inline_metadata:
        lines.extend(["Inline Metadata:"])
        for line_num, meta in inline_metadata:
            lines.append(f"  Line {line_num}: {meta}")

    return "\n".join(lines)
