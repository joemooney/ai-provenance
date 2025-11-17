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
@click.option("--template", type=str, default=None, help="Template to use (ieee830, simple)")
@click.option("--ai-tool", type=str, help="AI tool that generated this requirement")
@click.option("--ai-confidence", type=click.Choice(["high", "med", "low"]), help="AI confidence level")
@click.option("--parent", type=str, help="Parent requirement/epic ID")
def requirement_create(req_id: str, title: str, description: str, type: str, priority: str,
                       template: str | None, ai_tool: str | None, ai_confidence: str | None,
                       parent: str | None) -> None:
    """Create a new requirement."""
    from ai_provenance.requirements.manager import RequirementManager
    from ai_provenance.requirements.models import RequirementType, RequirementPriority
    from pathlib import Path

    try:
        manager = RequirementManager()

        # Determine AI generation status
        ai_generated = ai_tool is not None

        req = manager.create_requirement(
            req_id=req_id,
            title=title,
            description=description,
            req_type=RequirementType(type),
            priority=RequirementPriority(priority),
            ai_generated=ai_generated,
            ai_tool=ai_tool,
            parent=parent,
        )

        console.print(f"[green]✓[/green] Created requirement {req.id}: {req.title}")
        console.print(f"  Location: .ai-prov/requirements/{req.id}.json")

        # If template specified, also generate Markdown version
        if template:
            from ai_provenance.requirements.templates import requirement_to_markdown

            specs_dir = Path(".") / "specs" / "requirements"
            specs_dir.mkdir(parents=True, exist_ok=True)

            md_content = requirement_to_markdown(req, template)
            md_file = specs_dir / f"{req.id}.md"
            md_file.write_text(md_content)

            console.print(f"  Markdown: specs/requirements/{req.id}.md (from {template} template)")

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


@requirement.command("show")
@click.argument("req_id")
@click.option("--format", type=click.Choice(["text", "json", "md"]), default="text", help="Output format")
def requirement_show(req_id: str, format: str) -> None:
    """Show details of a requirement."""
    from ai_provenance.requirements.manager import RequirementManager
    from pathlib import Path
    import json

    try:
        manager = RequirementManager()
        req = manager.get_requirement(req_id)

        if not req:
            console.print(f"[red]✗[/red] Requirement {req_id} not found")
            raise click.Abort()

        if format == "json":
            console.print(req.model_dump_json(indent=2))
        elif format == "md":
            # Check if Markdown version exists
            md_file = Path(".") / "specs" / "requirements" / f"{req_id}.md"
            if md_file.exists():
                console.print(md_file.read_text())
            else:
                console.print(f"[yellow]![/yellow] No Markdown version found at {md_file}")
                console.print(f"[yellow]![/yellow] Use 'ai-prov requirement sync --json-to-md' to generate it")
        else:  # text
            console.print(f"\n[bold]{req.id}: {req.title}[/bold]\n")
            console.print(f"Type:        {req.type.value}")
            console.print(f"Status:      {req.status.value}")
            console.print(f"Priority:    {req.priority.value}")
            console.print(f"AI Generated: {req.ai_generated}")
            if req.ai_tool:
                console.print(f"AI Tool:     {req.ai_tool}")
            if req.parent:
                console.print(f"Parent:      {req.parent}")
            console.print(f"\n{req.description}\n")

            if req.files:
                console.print(f"[bold]Files ({len(req.files)}):[/bold]")
                for f in req.files:
                    console.print(f"  • {f}")

            if req.commits:
                console.print(f"\n[bold]Commits ({len(req.commits)}):[/bold]")
                for c in req.commits:
                    console.print(f"  • {c}")

            if req.tests:
                console.print(f"\n[bold]Tests ({len(req.tests)}):[/bold]")
                for t in req.tests:
                    console.print(f"  • {t}")

            if req.tags:
                console.print(f"\n[bold]Tags:[/bold] {', '.join(req.tags)}")

    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise click.Abort()


@requirement.command("sync")
@click.option("--md-to-json", is_flag=True, help="Sync Markdown requirements to JSON")
@click.option("--json-to-md", is_flag=True, help="Sync JSON requirements to Markdown")
@click.option("--template", type=str, default="ieee830", help="Template for JSON→MD sync")
@click.option("--quiet", is_flag=True, help="Suppress output")
def requirement_sync(md_to_json: bool, json_to_md: bool, template: str, quiet: bool) -> None:
    """Synchronize requirements between Markdown and JSON formats."""
    from ai_provenance.requirements.templates import sync_markdown_to_json, sync_json_to_markdown
    from pathlib import Path

    try:
        specs_dir = Path(".") / "specs" / "requirements"
        json_dir = Path(".") / ".ai-prov" / "requirements"

        # Ensure directories exist
        specs_dir.mkdir(parents=True, exist_ok=True)
        json_dir.mkdir(parents=True, exist_ok=True)

        # Default to md-to-json if neither specified
        if not md_to_json and not json_to_md:
            md_to_json = True

        if md_to_json:
            count = sync_markdown_to_json(specs_dir, json_dir)
            if not quiet:
                console.print(f"[green]✓[/green] Synced {count} Markdown → JSON")

        if json_to_md:
            count = sync_json_to_markdown(json_dir, specs_dir, template)
            if not quiet:
                console.print(f"[green]✓[/green] Synced {count} JSON → Markdown (template: {template})")

    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        import traceback
        if not quiet:
            console.print(traceback.format_exc())
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
            console.print("  • Use /trace to link code to requirements")
            console.print("  • Use /stamp to add AI metadata to files")
        else:
            console.print("\n[yellow]Run without --dry-run to create these files[/yellow]")

    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise click.Abort()


if __name__ == "__main__":
    cli()
