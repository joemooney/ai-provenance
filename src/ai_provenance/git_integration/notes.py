"""
Git notes management for provenance metadata.
"""

import json
from typing import Any, Dict, List, Optional

import git

from ai_provenance.core.models import CommitMetadata

NOTES_NAMESPACE = "ai-provenance"


def get_notes(
    commit_sha: str,
    namespace: str = NOTES_NAMESPACE,
    repo_path: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Get git note for a commit.

    Args:
        commit_sha: Commit SHA
        namespace: Notes namespace (default: ai-provenance)
        repo_path: Path to repository (default: current directory)

    Returns:
        Note content as dict, or None if no note exists
    """
    repo = git.Repo(repo_path or ".", search_parent_directories=True)

    try:
        note = repo.git.notes(f"--ref={namespace}", "show", commit_sha)
        return json.loads(note)
    except git.GitCommandError:
        return None
    except json.JSONDecodeError:
        # Note exists but is not valid JSON
        return {"raw": note}


def set_notes(
    commit_sha: str,
    metadata: Dict[str, Any],
    namespace: str = NOTES_NAMESPACE,
    force: bool = True,
    repo_path: Optional[str] = None,
) -> None:
    """
    Set git note for a commit.

    Args:
        commit_sha: Commit SHA
        metadata: Metadata to store
        namespace: Notes namespace (default: ai-provenance)
        force: Force overwrite if note exists
        repo_path: Path to repository (default: current directory)
    """
    repo = git.Repo(repo_path or ".", search_parent_directories=True)

    note_content = json.dumps(metadata, indent=2)

    args = [f"--ref={namespace}", "add"]
    if force:
        args.append("-f")
    args.extend(["-m", note_content, commit_sha])

    repo.git.notes(*args)


def list_commits_with_notes(
    namespace: str = NOTES_NAMESPACE,
    repo_path: Optional[str] = None,
) -> List[str]:
    """
    List all commits that have notes in the namespace.

    Args:
        namespace: Notes namespace (default: ai-provenance)
        repo_path: Path to repository (default: current directory)

    Returns:
        List of commit SHAs
    """
    repo = git.Repo(repo_path or ".", search_parent_directories=True)

    try:
        output = repo.git.notes(f"--ref={namespace}", "list")
        # Output format: <note-sha> <commit-sha>
        commits = []
        for line in output.strip().split("\n"):
            if line:
                parts = line.split()
                if len(parts) >= 2:
                    commits.append(parts[1])
        return commits
    except git.GitCommandError:
        return []


def remove_notes(
    commit_sha: str,
    namespace: str = NOTES_NAMESPACE,
    repo_path: Optional[str] = None,
) -> None:
    """
    Remove git note for a commit.

    Args:
        commit_sha: Commit SHA
        namespace: Notes namespace (default: ai-provenance)
        repo_path: Path to repository (default: current directory)
    """
    repo = git.Repo(repo_path or ".", search_parent_directories=True)

    try:
        repo.git.notes(f"--ref={namespace}", "remove", commit_sha)
    except git.GitCommandError:
        # Note doesn't exist
        pass


def get_ai_commits(
    since: Optional[str] = None,
    until: Optional[str] = None,
    repo_path: Optional[str] = None,
) -> List[tuple[str, CommitMetadata]]:
    """
    Get all commits with AI provenance metadata.

    Args:
        since: Start date/commit
        until: End date/commit
        repo_path: Path to repository (default: current directory)

    Returns:
        List of (commit_sha, metadata) tuples
    """
    repo = git.Repo(repo_path or ".", search_parent_directories=True)

    # Get all commits with notes
    commit_shas = list_commits_with_notes(repo_path=repo_path)

    results = []
    for sha in commit_shas:
        # Apply date filters if specified
        if since or until:
            commit = repo.commit(sha)
            commit_date = commit.committed_datetime

            if since:
                try:
                    since_commit = repo.commit(since)
                    if commit_date < since_commit.committed_datetime:
                        continue
                except Exception:
                    # Assume since is a date
                    pass

            if until:
                try:
                    until_commit = repo.commit(until)
                    if commit_date > until_commit.committed_datetime:
                        continue
                except Exception:
                    pass

        # Get metadata
        note_data = get_notes(sha, repo_path=repo_path)
        if note_data:
            try:
                metadata = CommitMetadata(**note_data)
                results.append((sha, metadata))
            except Exception:
                # Invalid metadata, skip
                pass

    return results
