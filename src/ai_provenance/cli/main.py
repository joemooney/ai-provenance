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


if __name__ == "__main__":
    cli()
