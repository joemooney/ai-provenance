"""
Repository initialization for AI provenance tracking.
"""

import os
import shutil
from pathlib import Path
from typing import Optional

import git


def initialize_repo(repo_path: Optional[str] = None, verbose: bool = False) -> None:
    """
    Initialize AI provenance tracking in a Git repository.

    Args:
        repo_path: Path to the repository (default: current directory)
        verbose: Enable verbose output

    Raises:
        git.InvalidGitRepositoryError: If not a valid Git repository
        FileExistsError: If already initialized
    """
    if repo_path is None:
        repo_path = os.getcwd()

    repo = git.Repo(repo_path, search_parent_directories=True)
    repo_root = Path(repo.working_dir)

    if verbose:
        print(f"Initializing AI provenance in: {repo_root}")

    # 1. Install git hooks
    _install_hooks(repo_root, verbose)

    # 2. Configure git filters
    _configure_filters(repo, verbose)

    # 3. Initialize git notes namespace
    _init_notes_namespace(repo, verbose)

    # 4. Create .gitattributes if needed
    _configure_gitattributes(repo_root, verbose)

    if verbose:
        print("✓ AI provenance tracking initialized!")


def _install_hooks(repo_root: Path, verbose: bool) -> None:
    """Install git hooks for provenance tracking."""
    hooks_dir = repo_root / ".git" / "hooks"
    hooks_dir.mkdir(exist_ok=True)

    # Get hook templates from package
    package_hooks = Path(__file__).parent.parent.parent.parent / "hooks"

    hooks_to_install = ["commit-msg", "post-commit", "pre-push"]

    for hook_name in hooks_to_install:
        hook_src = package_hooks / hook_name
        hook_dst = hooks_dir / hook_name

        if hook_dst.exists():
            if verbose:
                print(f"  Warning: {hook_name} already exists, backing up...")
            shutil.copy(hook_dst, hook_dst.with_suffix(".backup"))

        if hook_src.exists():
            shutil.copy(hook_src, hook_dst)
            hook_dst.chmod(0o755)
            if verbose:
                print(f"  ✓ Installed {hook_name} hook")
        else:
            if verbose:
                print(f"  ! {hook_name} template not found, skipping")


def _configure_filters(repo: git.Repo, verbose: bool) -> None:
    """Configure git filter driver for .meta.json generation."""
    config = repo.config_writer()

    # Add filter driver
    config.set_value('filter "ai-meta"', "clean", "ai-prov-filter clean")
    config.set_value('filter "ai-meta"', "smudge", "ai-prov-filter smudge")

    config.release()

    if verbose:
        print("  ✓ Configured git filter driver")


def _init_notes_namespace(repo: git.Repo, verbose: bool) -> None:
    """Initialize git notes namespace for AI provenance."""
    # Git notes are created on-demand, but we can verify the namespace is accessible
    try:
        # Try to list notes (will be empty initially)
        repo.git.notes("--ref=ai-provenance", "list")
        if verbose:
            print("  ✓ Git notes namespace 'ai-provenance' ready")
    except git.GitCommandError:
        # Namespace doesn't exist yet, but will be created on first note
        if verbose:
            print("  ✓ Git notes namespace 'ai-provenance' initialized")


def _configure_gitattributes(repo_root: Path, verbose: bool) -> None:
    """
    Create or update .gitattributes for auto-metadata generation.
    """
    gitattributes = repo_root / ".gitattributes"

    # Default file patterns to track
    patterns = [
        "*.py filter=ai-meta",
        "*.js filter=ai-meta",
        "*.ts filter=ai-meta",
        "*.tsx filter=ai-meta",
        "*.jsx filter=ai-meta",
        "*.java filter=ai-meta",
        "*.cpp filter=ai-meta",
        "*.c filter=ai-meta",
        "*.h filter=ai-meta",
        "*.go filter=ai-meta",
        "*.rs filter=ai-meta",
        "*.rb filter=ai-meta",
        "*.php filter=ai-meta",
    ]

    if gitattributes.exists():
        content = gitattributes.read_text()
        new_patterns = [p for p in patterns if p not in content]

        if new_patterns:
            with gitattributes.open("a") as f:
                f.write("\n# AI Provenance metadata generation\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
            if verbose:
                print(f"  ✓ Updated .gitattributes with {len(new_patterns)} new patterns")
    else:
        with gitattributes.open("w") as f:
            f.write("# AI Provenance metadata generation\n")
            for pattern in patterns:
                f.write(f"{pattern}\n")
        if verbose:
            print("  ✓ Created .gitattributes")


def is_initialized(repo_path: Optional[str] = None) -> bool:
    """
    Check if AI provenance is initialized in the repository.

    Args:
        repo_path: Path to the repository (default: current directory)

    Returns:
        True if initialized, False otherwise
    """
    if repo_path is None:
        repo_path = os.getcwd()

    try:
        repo = git.Repo(repo_path, search_parent_directories=True)
        repo_root = Path(repo.working_dir)

        # Check for hooks
        commit_msg_hook = repo_root / ".git" / "hooks" / "commit-msg"
        if not commit_msg_hook.exists():
            return False

        # Check for filter configuration
        config = repo.config_reader()
        try:
            config.get_value('filter "ai-meta"', "clean")
            return True
        except Exception:
            return False

    except git.InvalidGitRepositoryError:
        return False
