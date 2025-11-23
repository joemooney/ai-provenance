"""
Traceability matrix generation.
"""

import json
from collections import defaultdict
from pathlib import Path
from typing import Optional

import git

from ai_provenance.git_integration.notes import get_ai_commits
from ai_provenance import requirements as req_reader


def generate_trace_matrix(
    output_format: str = "md",
    repo_path: Optional[str] = None,
) -> str:
    """
    Generate a traceability matrix (features → code → tests).

    Args:
        output_format: Output format (md, json, html)
        repo_path: Path to repository (default: current directory)

    Returns:
        Formatted traceability matrix
    """
    repo = git.Repo(repo_path or ".", search_parent_directories=True)

    # Collect trace data
    trace_data = defaultdict(lambda: {"commits": [], "files": set(), "tests": set(), "ai_percent": 0})

    ai_commits = get_ai_commits(repo_path=repo.working_dir)

    for sha, metadata in ai_commits:
        if not metadata.trace:
            continue

        for trace_id in metadata.trace:
            trace_data[trace_id]["commits"].append(sha[:8])

            if metadata.files:
                trace_data[trace_id]["files"].update(metadata.files)

            if metadata.tests:
                trace_data[trace_id]["tests"].update(metadata.tests)

            # Track if AI-generated
            if metadata.ai_tool:
                trace_data[trace_id]["ai_percent"] += 1

    # Calculate AI percentages
    for trace_id, data in trace_data.items():
        total_commits = len(data["commits"])
        if total_commits > 0:
            data["ai_percent"] = (data["ai_percent"] / total_commits) * 100

    # Format output
    if output_format == "json":
        return _format_json_matrix(trace_data)
    elif output_format == "html":
        return _format_html_matrix(trace_data)
    else:
        return _format_markdown_matrix(trace_data)


def _format_markdown_matrix(trace_data: dict) -> str:
    """Format traceability matrix as Markdown table."""
    # Try to load requirements and mapping from requirements-manager
    try:
        requirements = req_reader.load_requirements()
        mapping = req_reader.load_mapping()

        # Create reverse mapping (SPEC-ID → requirement data)
        spec_to_req = {}
        for req in requirements:
            uuid = req.get("id")
            spec_id = mapping.get(uuid)
            if spec_id:
                spec_to_req[spec_id] = req
    except Exception:
        # If requirements.yaml doesn't exist, that's ok
        spec_to_req = {}

    lines = [
        "# Traceability Matrix",
        "",
        "| SPEC-ID | Title | Status | AI % | Commits | Files | Tests |",
        "|---------|-------|--------|------|---------|-------|-------|",
    ]

    for trace_id in sorted(trace_data.keys()):
        data = trace_data[trace_id]
        ai_pct = f"{data['ai_percent']:.0f}%"
        num_commits = len(data["commits"])
        num_files = len(data["files"])
        num_tests = len(data["tests"])

        # Get requirement details if available
        req = spec_to_req.get(trace_id, {})
        title = req.get("title", "Unknown")
        req_status = req.get("status", "Unknown")

        lines.append(
            f"| {trace_id} | {title} | {req_status} | {ai_pct} | {num_commits} | {num_files} | {num_tests} |"
        )

    lines.extend([
        "",
        "## Legend",
        "- **AI %**: Percentage of commits that used AI tools",
        "- **Commits**: Number of commits implementing this feature",
        "- **Files**: Number of files affected",
        "- **Tests**: Number of test cases covering this feature",
        "",
    ])

    return "\n".join(lines)


def _format_json_matrix(trace_data: dict) -> str:
    """Format traceability matrix as JSON."""
    # Convert sets to lists for JSON serialization
    json_data = {}
    for trace_id, data in trace_data.items():
        json_data[trace_id] = {
            "commits": data["commits"],
            "files": sorted(list(data["files"])),
            "tests": sorted(list(data["tests"])),
            "ai_percent": round(data["ai_percent"], 2),
        }

    return json.dumps(json_data, indent=2)


def _format_html_matrix(trace_data: dict) -> str:
    """Format traceability matrix as HTML table."""
    lines = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "  <title>Traceability Matrix</title>",
        "  <style>",
        "    table { border-collapse: collapse; width: 100%; }",
        "    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }",
        "    th { background-color: #4CAF50; color: white; }",
        "    tr:nth-child(even) { background-color: #f2f2f2; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <h1>Traceability Matrix</h1>",
        "  <table>",
        "    <tr>",
        "      <th>Feature</th>",
        "      <th>AI %</th>",
        "      <th>Commits</th>",
        "      <th>Files</th>",
        "      <th>Tests</th>",
        "      <th>Status</th>",
        "    </tr>",
    ]

    for trace_id in sorted(trace_data.keys()):
        data = trace_data[trace_id]
        ai_pct = f"{data['ai_percent']:.0f}%"
        num_commits = len(data["commits"])
        num_files = len(data["files"])
        num_tests = len(data["tests"])

        status = "Complete" if num_tests > 0 else "No tests"

        lines.append("    <tr>")
        lines.append(f"      <td>{trace_id}</td>")
        lines.append(f"      <td>{ai_pct}</td>")
        lines.append(f"      <td>{num_commits}</td>")
        lines.append(f"      <td>{num_files}</td>")
        lines.append(f"      <td>{num_tests}</td>")
        lines.append(f"      <td>{status}</td>")
        lines.append("    </tr>")

    lines.extend([
        "  </table>",
        "</body>",
        "</html>",
    ])

    return "\n".join(lines)
