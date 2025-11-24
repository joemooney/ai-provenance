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
@click.argument("paths", nargs=-1, type=click.Path())
@click.option("--ai-percent", is_flag=True, help="Show % of AI-generated code")
@click.option("--by-file", is_flag=True, help="Break down by file")
@click.option("--unreviewed", is_flag=True, help="Find unreviewed AI code")
@click.option("--trace", type=str, help="Find code for a requirement (e.g., SPEC-123)")
def query(paths: tuple, ai_percent: bool, by_file: bool, unreviewed: bool, trace: str | None) -> None:
    """
    Query repository for AI code metrics.

    PATHS: Optional file(s) or directory(ies) to query (default: entire repo)

    Examples:
        ai-prov query --ai-percent --by-file
        ai-prov query --ai-percent src/hello.py
        ai-prov query --ai-percent src/ tests/
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
            paths=list(paths) if paths else None,
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
# Requirements Integration Note
# ============================================================================
# Requirements management is handled by requirements-manager (Rust CLI).
# Use 'requirements-manager' commands to create/edit/list requirements.
# ai-provenance reads requirements from requirements.yaml and links them
# via SPEC-IDs in commit metadata.
#
# See INTEGRATION_v2.md for details.
# ============================================================================



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


# ============================================================================
# Initialization Wizard Commands
# ============================================================================


@cli.group()
def wizard() -> None:
    """Initialization wizard and project analysis."""
    pass


@wizard.command("init")
@click.option("--prompt-set", type=click.Choice(["quick", "standard", "comprehensive", "with_generation"]), default="standard")
def wizard_init(prompt_set: str) -> None:
    """Run initialization wizard to analyze existing project."""
    from ai_provenance.wizard.analyzer import InitializationWizard

    try:
        wizard = InitializationWizard()
        results = wizard.run_interactive()

        console.print(f"\n[green]✓[/green] Wizard analysis plan created")
        console.print(f"\nPrompt set: [bold]{prompt_set}[/bold]")
        console.print(f"Prompts to run: {len(results['prompts_to_run'])}\n")

        for prompt in results['prompts_to_run']:
            console.print(f"  📝 {prompt['name']}")

        console.print("\n[yellow]Next steps:[/yellow]")
        console.print("  1. Export prompts: ai-prov wizard export")
        console.print("  2. Feed prompts to an AI agent (Claude Code, Claude.ai, etc.)")
        console.print("  3. Save responses: ai-prov wizard apply <responses.json>")

    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise click.Abort()


@wizard.command("export")
@click.option("--output", default="init_prompts.json", help="Output file")
@click.option("--prompt-set", type=click.Choice(["quick", "standard", "comprehensive", "with_generation"]), default="standard")
def wizard_export(output: str, prompt_set: str) -> None:
    """Export initialization prompts for AI agent."""
    from ai_provenance.wizard.analyzer import InitializationWizard

    try:
        wizard = InitializationWizard()
        output_file = wizard.export_prompts(output)

        console.print(f"[green]✓[/green] Exported prompts to {output_file}")
        console.print("\n[bold]Usage with AI agents:[/bold]")
        console.print("  1. Open the JSON file and copy each prompt")
        console.print("  2. Feed to Claude Code, Claude.ai, or other AI")
        console.print("  3. Save responses in same JSON format")
        console.print("  4. Run: ai-prov wizard apply <responses.json>")

    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise click.Abort()


@wizard.command("scaffold")
@click.option("--dry-run", is_flag=True, help="Show what would be created without creating")
def wizard_scaffold(dry_run: bool) -> None:
    """Create recommended project structure."""
    from ai_provenance.wizard.structure import ProjectScaffolder

    try:
        scaffolder = ProjectScaffolder()

        if dry_run:
            console.print("[yellow]Dry run - showing what would be created:[/yellow]\n")

        # Create directory structure
        dirs_created = scaffolder.create_structure(dry_run=dry_run)
        for dir_msg in dirs_created:
            console.print(f"  {dir_msg}")

        # Create standard templates
        console.print("\n[bold]Standard templates:[/bold]")
        templates_created = scaffolder.create_standards_templates(dry_run=dry_run)
        for template_msg in templates_created:
            console.print(f"  {template_msg}")

        # Create Claude Code slash commands
        console.print("\n[bold]Claude Code slash commands:[/bold]")
        commands_created = scaffolder.create_claude_commands(dry_run=dry_run)
        for command_msg in commands_created:
            console.print(f"  {command_msg}")

        if not dry_run:
            console.print("\n[green]✓[/green] Project structure created")
            console.print("\n[yellow]Next steps:[/yellow]")
            console.print("  1. Review .standards/ templates")
            console.print("  2. Customize for your project")
            console.print("  3. Run: ai-prov wizard init")
            console.print("\n[bold]Claude Code integration:[/bold]")
            console.print("  • Use /req to create requirements interactively")
            console.print("  • Use /implement to build features from requirements")
            console.print("  • Use /trace to link code to requirements")
            console.print("  • Use /stamp to add AI metadata to files")
            console.print("  • Use /doc to generate and manage documentation")
        else:
            console.print("\n[yellow]Run without --dry-run to create these files[/yellow]")

    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise click.Abort()


# ============================================================================
# Documentation Commands
# ============================================================================


@cli.command()
@click.argument("guide", type=click.Choice(["user", "workflow", "walkthrough", "index"]), default="index", required=False)
@click.option("--dark", is_flag=True, help="Force dark mode (uses system preference by default)")
@click.option("--light", is_flag=True, help="Force light mode (uses system preference by default)")
@click.option("--regenerate", is_flag=True, help="Regenerate HTML from Markdown before opening")
def docs(guide: str, dark: bool, light: bool, regenerate: bool) -> None:
    """
    Open documentation in web browser.

    Available guides:
    - user: User guide (README)
    - workflow: Requirements workflow guide
    - walkthrough: Complete project setup walkthrough
    - index: Documentation index (default)
    """
    import webbrowser
    from pathlib import Path
    import subprocess
    import os

    # Find the repository root (works in dev and installed mode)
    # In dev: __file__ is .../ai-provenance/src/ai_provenance/cli/main.py
    # In installed: __file__ is .../site-packages/ai_provenance/cli/main.py
    current_file = Path(__file__).resolve()

    # Try to find repo root by looking for pyproject.toml
    repo_root = None
    for parent in [current_file.parent.parent.parent, current_file.parent.parent.parent.parent]:
        if (parent / "pyproject.toml").exists() and (parent / "docs" / "guides").exists():
            repo_root = parent
            break

    # If not found, check if we're in the source directory
    if repo_root is None:
        cwd = Path.cwd()
        if (cwd / "pyproject.toml").exists() and (cwd / "docs" / "guides").exists():
            repo_root = cwd
        elif (cwd.parent / "pyproject.toml").exists() and (cwd.parent / "docs" / "guides").exists():
            repo_root = cwd.parent

    if repo_root is None:
        console.print("[red]✗[/red] Could not find documentation directory.")
        console.print("\nThe docs command only works when run from the ai-provenance repository.")
        console.print("Visit: https://github.com/joemooney/ai-provenance/tree/master/docs/guides")
        raise click.Abort()

    # Regenerate if requested (only in dev mode)
    if regenerate:
        script = repo_root / "helper" / "generate_docs.py"
        if script.exists():
            try:
                console.print("Regenerating documentation...")
                subprocess.run(["python", str(script)], check=True, cwd=str(repo_root))
                console.print("[green]✓[/green] Documentation regenerated")
            except Exception as e:
                console.print(f"[yellow]⚠[/yellow] Could not regenerate docs: {e}")
        else:
            console.print("[yellow]⚠[/yellow] Can only regenerate in development mode (helper script not found)")

    # Map guide names to HTML files
    guide_map = {
        "user": "user-guide.html",
        "workflow": "requirements-workflow.html",
        "walkthrough": "walkthrough.html",
        "index": "index.html",
    }

    # Get the HTML file path
    html_file = repo_root / "docs" / "guides" / guide_map[guide]

    if not html_file.exists():
        console.print(f"[red]✗[/red] Documentation file not found: {html_file}")
        console.print("\nAvailable in repository at: docs/guides/")
        console.print("Visit: https://github.com/joemooney/ai-provenance/tree/master/docs/guides")
        raise click.Abort()

    # Handle dark/light mode preference
    # Note: The HTML already uses @media (prefers-color-scheme: dark)
    # We can't force it without modifying the HTML or using browser flags
    if dark and light:
        console.print("[yellow]⚠[/yellow] Cannot use both --dark and --light. Using system preference.")
    elif dark:
        console.print("[dim]Note: Dark mode is controlled by system preferences in the HTML.[/dim]")
    elif light:
        console.print("[dim]Note: Light mode is controlled by system preferences in the HTML.[/dim]")

    # Open in browser
    try:
        file_url = f"file://{html_file.absolute()}"
        console.print(f"Opening [bold]{guide}[/bold] guide in browser...")
        webbrowser.open(file_url)
        console.print(f"[green]✓[/green] Opened: {file_url}")
    except Exception as e:
        console.print(f"[red]✗[/red] Could not open browser: {e}")
        console.print(f"\nManually open: {html_file}")
        raise click.Abort()


if __name__ == "__main__":
    cli()
