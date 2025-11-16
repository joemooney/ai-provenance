"""
Repository validation for AI provenance metadata.
"""

from pathlib import Path
from typing import List, Optional

import git

from ai_provenance.git_integration.notes import get_ai_commits
from ai_provenance.parsers.stamper import parse_inline_metadata


def validate_repo(
    require_review: bool = False,
    require_tests: bool = False,
    repo_path: Optional[str] = None,
) -> List[str]:
    """
    Validate repository metadata integrity.

    Args:
        require_review: Ensure all AI code is reviewed
        require_tests: Ensure all traced code has tests
        repo_path: Path to repository (default: current directory)

    Returns:
        List of validation errors (empty if validation passes)
    """
    repo = git.Repo(repo_path or ".", search_parent_directories=True)
    errors = []

    # Get all AI commits
    ai_commits = get_ai_commits(repo_path=repo.working_dir)

    # Validate review requirement
    if require_review:
        for sha, metadata in ai_commits:
            if not metadata.reviewed_by:
                commit = repo.commit(sha)
                errors.append(
                    f"Commit {sha[:8]} has AI code but no review: {commit.message.split()[0][:50]}"
                )

    # Validate test coverage requirement
    if require_tests:
        for sha, metadata in ai_commits:
            if metadata.trace and not metadata.tests:
                commit = repo.commit(sha)
                traces = ", ".join(metadata.trace)
                errors.append(
                    f"Commit {sha[:8]} has traces ({traces}) but no test coverage: {commit.message.split()[0][:50]}"
                )

    # Validate inline metadata consistency
    repo_root = Path(repo.working_dir)
    tracked_files = repo.git.ls_files().split("\n")

    for file_path in tracked_files:
        full_path = repo_root / file_path

        if not full_path.exists() or not full_path.is_file():
            continue

        try:
            metadata = parse_inline_metadata(str(full_path))
            for line_num, meta in metadata:
                # Check for required fields
                if "tool" not in meta:
                    errors.append(f"{file_path}:{line_num} - Missing AI tool in metadata")

                if "confidence" not in meta:
                    errors.append(f"{file_path}:{line_num} - Missing confidence level")

                # Check review requirement
                if require_review and "reviewed" not in meta:
                    errors.append(f"{file_path}:{line_num} - AI code not reviewed")

        except Exception as e:
            errors.append(f"{file_path} - Error parsing metadata: {e}")

    return errors
