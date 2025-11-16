"""
Repository-wide queries for AI metadata.
"""

import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

import git

from ai_provenance.git_integration.notes import get_ai_commits
from ai_provenance.parsers.stamper import parse_inline_metadata


def run_query(
    ai_percent: bool = False,
    by_file: bool = False,
    unreviewed: bool = False,
    trace: Optional[str] = None,
    repo_path: Optional[str] = None,
) -> str:
    """
    Run queries on repository AI metadata.

    Args:
        ai_percent: Show % of AI-generated code
        by_file: Break down metrics by file
        unreviewed: Find unreviewed AI code
        trace: Find code for a requirement
        repo_path: Path to repository (default: current directory)

    Returns:
        Formatted query results
    """
    repo = git.Repo(repo_path or ".", search_parent_directories=True)

    if ai_percent:
        return _query_ai_percentage(repo, by_file)
    elif unreviewed:
        return _query_unreviewed(repo)
    elif trace:
        return _query_trace(repo, trace)
    else:
        return "No query specified. Use --ai-percent, --unreviewed, or --trace"


def _query_ai_percentage(repo: git.Repo, by_file: bool) -> str:
    """Calculate % of AI-generated code."""
    repo_root = Path(repo.working_dir)

    # Get all tracked files
    tracked_files = repo.git.ls_files().split("\n")

    total_lines = 0
    ai_lines = 0
    file_stats = {}

    for file_path in tracked_files:
        full_path = repo_root / file_path

        if not full_path.exists() or not full_path.is_file():
            continue

        # Count total lines
        try:
            lines = full_path.read_text().split("\n")
            file_total = len(lines)
            total_lines += file_total

            # Count AI lines from inline metadata
            metadata = parse_inline_metadata(str(full_path))
            file_ai = sum(1 for _ in metadata)  # Simplified: each metadata line counts
            ai_lines += file_ai

            if by_file:
                file_stats[file_path] = {
                    "total": file_total,
                    "ai": file_ai,
                    "percent": (file_ai / file_total * 100) if file_total > 0 else 0,
                }

        except Exception:
            # Skip files that can't be read
            continue

    overall_percent = (ai_lines / total_lines * 100) if total_lines > 0 else 0

    # Format output
    lines = [f"AI-Generated Code: {overall_percent:.2f}%", f"  Total lines: {total_lines:,}", f"  AI lines: {ai_lines:,}", ""]

    if by_file and file_stats:
        lines.append("By File:")
        # Sort by AI percentage
        sorted_files = sorted(
            file_stats.items(), key=lambda x: x[1]["percent"], reverse=True
        )
        for file_path, stats in sorted_files[:20]:  # Top 20
            if stats["ai"] > 0:
                lines.append(f"  {file_path}: {stats['percent']:.1f}% ({stats['ai']}/{stats['total']})")

    return "\n".join(lines)


def _query_unreviewed(repo: git.Repo) -> str:
    """Find unreviewed AI code."""
    # Get all AI commits
    ai_commits = get_ai_commits(repo_path=repo.working_dir)

    unreviewed = []
    for sha, metadata in ai_commits:
        if not metadata.reviewed_by:
            commit = repo.commit(sha)
            unreviewed.append({
                "sha": sha[:8],
                "message": commit.message.split("\n")[0],
                "date": commit.committed_datetime.strftime("%Y-%m-%d"),
                "tool": metadata.ai_tool.value if metadata.ai_tool else "unknown",
            })

    if not unreviewed:
        return "✓ No unreviewed AI code found"

    lines = [f"Found {len(unreviewed)} unreviewed AI commits:", ""]
    for commit_info in unreviewed:
        lines.append(
            f"  {commit_info['sha']} ({commit_info['date']}) [{commit_info['tool']}] {commit_info['message']}"
        )

    return "\n".join(lines)


def _query_trace(repo: git.Repo, trace_id: str) -> str:
    """Find code for a requirement."""
    # Get all AI commits
    ai_commits = get_ai_commits(repo_path=repo.working_dir)

    matching_commits = []
    for sha, metadata in ai_commits:
        if metadata.trace and trace_id in metadata.trace:
            commit = repo.commit(sha)
            matching_commits.append({
                "sha": sha[:8],
                "message": commit.message.split("\n")[0],
                "date": commit.committed_datetime.strftime("%Y-%m-%d"),
                "files": metadata.files or [],
            })

    if not matching_commits:
        return f"No commits found for {trace_id}"

    lines = [f"Commits for {trace_id}:", ""]
    for commit_info in matching_commits:
        lines.append(f"  {commit_info['sha']} ({commit_info['date']}) {commit_info['message']}")
        if commit_info["files"]:
            for file in commit_info["files"]:
                lines.append(f"    - {file}")

    return "\n".join(lines)
