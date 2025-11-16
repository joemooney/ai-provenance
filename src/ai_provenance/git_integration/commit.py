"""
Git commit operations with provenance metadata.
"""

import json
from datetime import datetime
from typing import List, Optional

import git

from ai_provenance.core.models import AITool, CommitMetadata, Confidence


def create_provenance_commit(
    message: str,
    tool: Optional[str] = None,
    confidence: Optional[str] = None,
    trace: Optional[List[str]] = None,
    tests: Optional[List[str]] = None,
    reviewer: Optional[str] = None,
    repo_path: Optional[str] = None,
) -> str:
    """
    Create a commit with structured provenance metadata.

    Args:
        message: Commit message (can include AI tag and metadata)
        tool: AI tool used
        confidence: Confidence level (high, med, low)
        trace: Requirement IDs
        tests: Test case IDs
        reviewer: Reviewer email
        repo_path: Path to repository (default: current directory)

    Returns:
        Commit SHA

    Raises:
        git.GitCommandError: If commit fails
        ValueError: If invalid parameters
    """
    repo = git.Repo(repo_path or ".", search_parent_directories=True)

    # Build structured commit message
    full_message = _build_commit_message(
        message=message,
        tool=tool,
        confidence=confidence,
        trace=trace,
        tests=tests,
        reviewer=reviewer,
    )

    # Stage changes
    if repo.is_dirty(untracked_files=False):
        repo.git.add("-u")  # Add modified files

    # Create commit
    commit = repo.index.commit(full_message)

    # Add git note with metadata
    if tool or trace or tests or reviewer:
        metadata = _build_commit_metadata(
            tool=tool,
            confidence=confidence,
            trace=trace,
            tests=tests,
            reviewer=reviewer,
        )
        _add_commit_note(repo, commit.hexsha, metadata)

    return commit.hexsha


def _build_commit_message(
    message: str,
    tool: Optional[str],
    confidence: Optional[str],
    trace: Optional[List[str]],
    tests: Optional[List[str]],
    reviewer: Optional[str],
) -> str:
    """Build structured commit message."""
    parts = []

    # Add AI tag if tool provided
    if tool:
        tag = f"[AI:{tool}:{confidence or 'med'}]"
        # Check if message already has AI tag
        if not message.strip().startswith("[AI:"):
            parts.append(f"{tag} {message}")
        else:
            parts.append(message)
    else:
        parts.append(message)

    # Add metadata footer
    if trace:
        parts.append(f"Trace: {', '.join(trace)}")

    if tests:
        parts.append(f"Test: {', '.join(tests)}")

    if reviewer:
        reviewed_by = reviewer if reviewer.startswith("AI+") else f"AI+{reviewer}"
        parts.append(f"Reviewed-by: {reviewed_by}")

    return "\n".join(parts)


def _build_commit_metadata(
    tool: Optional[str],
    confidence: Optional[str],
    trace: Optional[List[str]],
    tests: Optional[List[str]],
    reviewer: Optional[str],
) -> CommitMetadata:
    """Build commit metadata object."""
    return CommitMetadata(
        ai_tool=AITool(tool) if tool else None,
        confidence=Confidence(confidence) if confidence else None,
        trace=trace,
        tests=tests,
        reviewed_by=reviewer,
        reviewed_at=datetime.utcnow() if reviewer else None,
    )


def _add_commit_note(repo: git.Repo, commit_sha: str, metadata: CommitMetadata) -> None:
    """Add git note with commit metadata."""
    note_content = metadata.model_dump_json(indent=2, exclude_none=True)

    # Add note to ai-provenance namespace
    repo.git.notes("--ref=ai-provenance", "add", "-f", "-m", note_content, commit_sha)


def get_commit_metadata(commit_sha: str, repo_path: Optional[str] = None) -> Optional[CommitMetadata]:
    """
    Get provenance metadata for a commit.

    Args:
        commit_sha: Commit SHA
        repo_path: Path to repository (default: current directory)

    Returns:
        CommitMetadata if found, None otherwise
    """
    repo = git.Repo(repo_path or ".", search_parent_directories=True)

    try:
        note = repo.git.notes("--ref=ai-provenance", "show", commit_sha)
        data = json.loads(note)
        return CommitMetadata(**data)
    except git.GitCommandError:
        # No note found
        return None
