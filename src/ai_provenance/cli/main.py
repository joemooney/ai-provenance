"""
Main CLI entry point for ai-provenance.
"""

import click
from rich.console import Console

from ai_provenance import __version__

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="ai-prov")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """
    AI Provenance - Git-native AI code provenance and metadata tracking.

    Track, attribute, and audit AI-generated code with hierarchical metadata
    at line, block, function, and file levels.
    """
    ctx.ensure_object(dict)


@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def init(verbose: bool) -> None:
    """
    Initialize AI provenance tracking in the current repository.

    Sets up:
    - Git hooks for automatic metadata tracking
    - Filter driver for .meta.json generation
    - Git notes namespace for provenance data
    """
    from ai_provenance.git_integration.init import initialize_repo

    try:
        initialize_repo(verbose=verbose)
        console.print("[green]✓[/green] AI provenance tracking initialized!")
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise click.Abort()


@cli.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--tool", type=str, required=True, help="AI tool used (claude, copilot, etc.)")
@click.option(
    "--conf",
    "--confidence",
    type=click.Choice(["high", "med", "low"]),
    required=True,
    help="Confidence level",
)
@click.option("--trace", multiple=True, help="Requirement IDs (e.g., SPEC-123)")
@click.option("--test", multiple=True, help="Test case IDs (e.g., TC-456)")
@click.option("--reviewer", type=str, help="Reviewer email")
def stamp(
    file: str, tool: str, conf: str, trace: tuple, test: tuple, reviewer: str | None
) -> None:
    """
    Add AI metadata inline comments to a file.

    Example:
        ai-prov stamp src/auth.py --tool claude --conf high \\
            --trace SPEC-89 --test TC-210 --reviewer alice@example.com
    """
    from ai_provenance.parsers.stamper import stamp_file

    try:
        stamp_file(
            file_path=file,
            tool=tool,
            confidence=conf,
            trace=list(trace) if trace else None,
            tests=list(test) if test else None,
            reviewer=reviewer,
        )
        console.print(f"[green]✓[/green] Stamped {file}")
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise click.Abort()


@cli.command()
@click.option("-m", "--message", required=True, help="Commit message")
@click.option("--tool", type=str, help="AI tool used")
@click.option("--conf", type=click.Choice(["high", "med", "low"]), help="Confidence level")
@click.option("--trace", multiple=True, help="Requirement IDs")
@click.option("--test", multiple=True, help="Test case IDs")
@click.option("--reviewer", type=str, help="Reviewer email")
def commit(
    message: str,
    tool: str | None,
    conf: str | None,
    trace: tuple,
    test: tuple,
    reviewer: str | None,
) -> None:
    """
    Create a commit with structured provenance metadata.

    Example:
        ai-prov commit -m "feat(auth): add JWT refresh" \\
            --tool claude --conf high --trace SPEC-89
    """
    from ai_provenance.git_integration.commit import create_provenance_commit

    try:
        create_provenance_commit(
            message=message,
            tool=tool,
            confidence=conf,
            trace=list(trace) if trace else None,
            tests=list(test) if test else None,
            reviewer=reviewer,
        )
        console.print("[green]✓[/green] Commit created with provenance metadata")
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise click.Abort()


@cli.command()
@click.argument("file", type=click.Path())
@click.option("--rev", default="HEAD", help="Git revision (default: HEAD)")
@click.option("--format", type=click.Choice(["json", "md", "text"]), default="text")
def report(file: str, rev: str, format: str) -> None:
    """
    Generate a comprehensive metadata report for a file.

    Example:
        ai-prov report src/auth.py --rev HEAD~3 --format md
    """
    from ai_provenance.reporters.file_report import generate_file_report

    try:
        output = generate_file_report(file_path=file, revision=rev, output_format=format)
        console.print(output)
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise click.Abort()


@cli.command()
@click.option("--ai-percent", is_flag=True, help="Show % of AI-generated code")
@click.option("--by-file", is_flag=True, help="Break down by file")
@click.option("--unreviewed", is_flag=True, help="Find unreviewed AI code")
@click.option("--trace", type=str, help="Find code for a requirement (e.g., SPEC-123)")
def query(ai_percent: bool, by_file: bool, unreviewed: bool, trace: str | None) -> None:
    """
    Query repository for AI code metrics.

    Examples:
        ai-prov query --ai-percent --by-file
        ai-prov query --unreviewed
        ai-prov query --trace SPEC-89
    """
    from ai_provenance.reporters.query import run_query

    try:
        result = run_query(
            ai_percent=ai_percent,
            by_file=by_file,
            unreviewed=unreviewed,
            trace=trace,
        )
        console.print(result)
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise click.Abort()


@cli.command()
@click.option("--require-review", is_flag=True, help="Ensure all AI code is reviewed")
@click.option("--require-tests", is_flag=True, help="Ensure all traced code has tests")
def validate(require_review: bool, require_tests: bool) -> None:
    """
    Validate repository metadata integrity.

    Example:
        ai-prov validate --require-review --require-tests
    """
    from ai_provenance.reporters.validator import validate_repo

    try:
        errors = validate_repo(require_review=require_review, require_tests=require_tests)
        if errors:
            for error in errors:
                console.print(f"[red]✗[/red] {error}")
            raise click.Abort()
        else:
            console.print("[green]✓[/green] Repository validation passed")
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise click.Abort()


@cli.command("trace-matrix")
@click.option("--format", type=click.Choice(["md", "json", "html"]), default="md")
@click.option("--output", type=click.Path(), help="Output file (default: stdout)")
def trace_matrix(format: str, output: str | None) -> None:
    """
    Generate a traceability matrix (features → code → tests).

    Example:
        ai-prov trace-matrix --format md > TRACEABILITY.md
    """
    from ai_provenance.reporters.traceability import generate_trace_matrix

    try:
        result = generate_trace_matrix(output_format=format)
        if output:
            with open(output, "w") as f:
                f.write(result)
            console.print(f"[green]✓[/green] Traceability matrix written to {output}")
        else:
            console.print(result)
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise click.Abort()


# ============================================================================
# Requirements Management Commands
# ============================================================================


@cli.group()
def requirement() -> None:
    """Requirements management and traceability."""
    pass


@requirement.command("create")
@click.argument("req_id")
@click.option("--title", required=True, help="Requirement title")
@click.option("--description", required=True, help="Requirement description")
@click.option("--type", type=click.Choice(["feature", "bug", "enhancement", "refactor"]), default="feature")
@click.option("--priority", type=click.Choice(["critical", "high", "medium", "low"]), default="medium")
def requirement_create(req_id: str, title: str, description: str, type: str, priority: str) -> None:
    """Create a new requirement."""
    from ai_provenance.requirements.manager import RequirementManager
    from ai_provenance.requirements.models import RequirementType, RequirementPriority

    try:
        manager = RequirementManager()
        req = manager.create_requirement(
            req_id=req_id,
            title=title,
            description=description,
            req_type=RequirementType(type),
            priority=RequirementPriority(priority),
        )
        console.print(f"[green]✓[/green] Created requirement {req.id}: {req.title}")
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise click.Abort()


@requirement.command("link")
@click.argument("req_id")
@click.option("--file", type=str, help="Link a file to this requirement")
@click.option("--commit", type=str, help="Link a commit to this requirement")
@click.option("--test", type=str, help="Link a test case to this requirement")
def requirement_link(req_id: str, file: str | None, commit: str | None, test: str | None) -> None:
    """Link files, commits, or tests to a requirement."""
    from ai_provenance.requirements.manager import RequirementManager

    try:
        manager = RequirementManager()

        if file:
            manager.link_file(req_id, file)
            console.print(f"[green]✓[/green] Linked file {file} to {req_id}")

        if commit:
            manager.link_commit(req_id, commit)
            console.print(f"[green]✓[/green] Linked commit {commit} to {req_id}")

        if test:
            manager.link_test(req_id, test)
            console.print(f"[green]✓[/green] Linked test {test} to {req_id}")

    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise click.Abort()


@requirement.command("list")
@click.option("--status", type=str, help="Filter by status")
def requirement_list(status: str | None) -> None:
    """List all requirements."""
    from ai_provenance.requirements.manager import RequirementManager
    from ai_provenance.requirements.models import RequirementStatus

    try:
        manager = RequirementManager()
        status_filter = RequirementStatus(status) if status else None
        requirements = manager.list_requirements(status=status_filter)

        if not requirements:
            console.print("No requirements found")
            return

        console.print(f"\n[bold]Requirements ({len(requirements)}):[/bold]\n")
        for req in requirements:
            status_color = {
                "planned": "blue",
                "in-progress": "yellow",
                "implemented": "green",
                "tested": "green",
                "verified": "green",
            }.get(req.status.value, "white")

            console.print(
                f"  [{status_color}]{req.id}[/{status_color}] - {req.title} "
                f"([{status_color}]{req.status.value}[/{status_color}])"
            )

    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise click.Abort()


# ============================================================================
# Prompt Management Commands
# ============================================================================


@cli.group()
def prompt() -> None:
    """Prompt storage and management."""
    pass


@prompt.command("store")
@click.option("--file", type=str, help="File this prompt generated/modified")
@click.option("--prompt", required=True, help="The prompt text")
@click.option("--trace", multiple=True, help="Requirement IDs")
@click.option("--test", multiple=True, help="Test case IDs")
@click.option("--tool", default="claude", help="AI tool used")
@click.option("--conf", "--confidence", type=click.Choice(["high", "med", "low"]), default="high")
def prompt_store(file: str | None, prompt: str, trace: tuple, test: tuple, tool: str, conf: str) -> None:
    """Store a prompt used to generate code."""
    from ai_provenance.prompts.storage import PromptStore
    from ai_provenance.prompts.models import PromptType

    try:
        store = PromptStore()
        stored_prompt = store.create_from_text(
            prompt_text=prompt,
            file_path=file,
            requirement_ids=list(trace) if trace else None,
            test_ids=list(test) if test else None,
            ai_tool=tool,
            confidence=conf,
        )

        console.print(f"[green]✓[/green] Stored prompt {stored_prompt.id}")
        if file:
            console.print(f"  Linked to file: {file}")

    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise click.Abort()


@prompt.command("list")
@click.option("--file", type=str, help="List prompts for a specific file")
@click.option("--trace", type=str, help="List prompts for a requirement")
def prompt_list(file: str | None, trace: str | None) -> None:
    """List stored prompts."""
    from ai_provenance.prompts.storage import PromptStore

    try:
        store = PromptStore()

        if file:
            prompts = store.list_for_file(file)
            console.print(f"\n[bold]Prompts for {file}:[/bold]\n")
        elif trace:
            prompts = store.list_for_requirement(trace)
            console.print(f"\n[bold]Prompts for {trace}:[/bold]\n")
        else:
            # List all prompts
            prompts = [store.get(p.stem) for p in store.prompts_dir.glob("*.json")]
            console.print(f"\n[bold]All Prompts ({len(prompts)}):[/bold]\n")

        for p in prompts:
            if p:
                console.print(f"  {p.id} - {p.timestamp}")
                console.print(f"    {p.prompt_text[:80]}...")

    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise click.Abort()


# ============================================================================
# Feature Management Commands
# ============================================================================


@cli.group()
def features() -> None:
    """Feature flags management."""
    pass


@features.command("list")
def features_list() -> None:
    """List all features and their status."""
    from ai_provenance.core.features import load_feature_config

    try:
        feature_set = load_feature_config()

        console.print("\n[bold]AI Provenance Features:[/bold]\n")

        for feature, config in feature_set.features.items():
            status_symbol = "✓" if config.enabled else "○"
            status_color = "green" if config.enabled else "dim"

            console.print(
                f"  [{status_color}]{status_symbol}[/{status_color}] "
                f"[bold]{feature.value}[/bold] ({config.status.value})"
            )
            console.print(f"     {config.description}")

    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise click.Abort()


@features.command("enable")
@click.argument("feature_names", nargs=-1, required=True)
def features_enable(feature_names: tuple) -> None:
    """Enable one or more features."""
    from ai_provenance.core.features import load_feature_config, save_feature_config, Feature

    try:
        feature_set = load_feature_config()

        for name in feature_names:
            feature = Feature(name)
            feature_set.enable(feature)
            console.print(f"[green]✓[/green] Enabled {name}")

        save_feature_config(feature_set)

    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise click.Abort()


@features.command("disable")
@click.argument("feature_names", nargs=-1, required=True)
def features_disable(feature_names: tuple) -> None:
    """Disable one or more features."""
    from ai_provenance.core.features import load_feature_config, save_feature_config, Feature

    try:
        feature_set = load_feature_config()

        for name in feature_names:
            feature = Feature(name)
            feature_set.disable(feature)
            console.print(f"[yellow]○[/yellow] Disabled {name}")

        save_feature_config(feature_set)

    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise click.Abort()


@features.command("profile")
@click.argument("profile_name")
def features_profile(profile_name: str) -> None:
    """Apply a feature profile (minimal, standard, full, team, research, regeneration)."""
    from ai_provenance.core.features import load_feature_config, save_feature_config

    try:
        feature_set = load_feature_config()
        feature_set.apply_profile(profile_name)
        save_feature_config(feature_set)

        console.print(f"[green]✓[/green] Applied profile '{profile_name}'")

        # Show enabled features
        enabled = feature_set.get_enabled_features()
        console.print(f"\nEnabled features ({len(enabled)}):")
        for feature in enabled:
            console.print(f"  ✓ {feature.value}")

    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise click.Abort()


if __name__ == "__main__":
    cli()
