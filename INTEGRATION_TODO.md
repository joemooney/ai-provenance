# AI-Provenance Integration TODO

## What's Been Done ✅

1. **Removed native requirements module**
   - `src/ai_provenance/requirements/` (manager, models, templates) → moved to `requirements_OLD_BACKUP/`
   - Removed requirement CLI commands from `cli/main.py`

2. **Added lightweight requirements reader**
   - Created `src/ai_provenance/requirements.py` (~150 lines)
   - Functions to read `requirements.yaml` and `.requirements-mapping.yaml`

3. **Updated traceability reporter**
   - `src/ai_provenance/reporters/traceability.py` now reads requirements from requirements-manager
   - Shows SPEC-ID, Title, and Status in trace matrix

## What Still Needs to Be Done ⬜

### 1. Fix Import Issues

**Problem**: The codebase still has imports referencing the old `requirements` module.

**Files to check and update**:
```bash
# Find all remaining imports
grep -r "from ai_provenance.requirements" src/
grep -r "import.*requirements\.manager" src/
grep -r "import.*requirements\.models" src/
```

**Action**:
- Remove or update any imports of the old requirements module
- If functionality is needed, use the new `requirements.py` reader instead

### 2. Update Tests

**Problem**: Tests may reference the old requirements module.

**Files to check**:
```bash
# Find test files referencing requirements
grep -r "requirements" tests/
```

**Action**:
- Update or remove tests that depend on the old requirements module
- Add new tests for the `requirements.py` reader if needed

### 3. Update Documentation

**Files to update**:
- `README.md` - Add section on requirements-manager integration
- `REQUIREMENTS.md` - Note that SPEC-002 is now fulfilled via requirements-manager
- `.ai-prov/config.yaml` - Add configuration for requirements source (if config exists)

**Content to add to README**:
```markdown
## Requirements Management

AI Provenance integrates with [requirements-manager](https://github.com/joemooney/req) for requirements tracking.

### Setup

1. Install requirements-manager:
   ```bash
   git clone https://github.com/joemooney/req
   cd req/requirements-manager
   cargo install --path .
   ```

2. Register your project:
   ```bash
   requirements-manager db register \
     --name my-project \
     --path $(pwd)/requirements.yaml
   ```

3. Create requirements:
   ```bash
   requirements-manager add -i
   ```

4. Generate SPEC-ID mapping:
   ```bash
   requirements-manager export --format mapping
   ```

### Usage

Link commits to requirements using SPEC-IDs:
```bash
ai-prov stamp src/file.py --tool claude --conf high --trace SPEC-001
ai-prov commit -m "feat: implement feature" --trace SPEC-001
```

Generate traceability matrix:
```bash
ai-prov trace-matrix
```

See [INTEGRATION_v2.md](INTEGRATION_v2.md) for complete details.
```

### 4. Remove Old Backup Directory

**Action**:
```bash
# After verifying nothing is needed from backup
rm -rf src/ai_provenance/requirements_OLD_BACKUP/
```

### 5. Update Dependencies

**Check**: Does `pyproject.toml` or `requirements.txt` have dependencies only used by the old requirements module?

**Possible removals** (if not used elsewhere):
- Pydantic (if only used for old requirements models)
- Any other dependencies specific to the old requirements module

**Keep**:
- PyYAML (needed to read requirements.yaml)

### 6. Verify All Commands Work

**Test these commands**:
```bash
# Should work (don't use requirements module)
ai-prov init
ai-prov stamp FILE --tool claude --conf high --trace SPEC-001
ai-prov commit -m "test" --trace SPEC-001
ai-prov query --ai-percent
ai-prov report FILE
ai-prov validate
ai-prov trace-matrix

# Should be removed or error gracefully
ai-prov requirement create  # Should not exist
ai-prov requirement list     # Should not exist
```

### 7. Update .gitignore

**Add**:
```
# Requirements manager integration
requirements.yaml
.requirements-mapping.yaml
```

**Reasoning**: These files are project-specific, not part of ai-provenance itself.

### 8. Optional: Add Helper Commands

**Consider adding**:

A command to check if requirements-manager is installed and configured:
```python
@cli.command()
def check_requirements() -> None:
    """Check requirements-manager integration status."""
    import subprocess
    from pathlib import Path

    # Check if requirements-manager is installed
    try:
        result = subprocess.run(
            ["requirements-manager", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            console.print("[green]✓[/green] requirements-manager is installed")
        else:
            console.print("[yellow]⚠[/yellow] requirements-manager not found in PATH")
    except FileNotFoundError:
        console.print("[red]✗[/red] requirements-manager not installed")
        console.print("Install: https://github.com/joemooney/req")

    # Check for requirements.yaml
    if Path("requirements.yaml").exists():
        console.print("[green]✓[/green] requirements.yaml found")
    else:
        console.print("[yellow]⚠[/yellow] requirements.yaml not found")
        console.print("Create requirements: requirements-manager add -i")

    # Check for mapping file
    if Path(".requirements-mapping.yaml").exists():
        console.print("[green]✓[/green] .requirements-mapping.yaml found")
    else:
        console.print("[yellow]⚠[/yellow] .requirements-mapping.yaml not found")
        console.print("Generate mapping: requirements-manager export --format mapping")
```

## Summary Prompt for Claude Code

Use this prompt:

---

**Prompt:**

I've partially integrated ai-provenance with requirements-manager (a Rust CLI for requirements management). Here's what's been done:

1. Removed old requirements module (moved to `requirements_OLD_BACKUP/`)
2. Created new lightweight reader: `src/ai_provenance/requirements.py`
3. Updated traceability reporter to read from `requirements.yaml`
4. Removed requirement CLI commands

Please complete the integration:

1. **Find and fix broken imports**: Search for any remaining imports of the old `requirements` module and remove/update them.

2. **Update documentation**: Add a "Requirements Management" section to README.md explaining the integration with requirements-manager (see INTEGRATION_v2.md for details).

3. **Clean up**: Remove `src/ai_provenance/requirements_OLD_BACKUP/` directory after confirming nothing is needed.

4. **Update .gitignore**: Add `requirements.yaml` and `.requirements-mapping.yaml`.

5. **Test**: Verify these commands work:
   - `ai-prov trace-matrix` (should read from requirements.yaml if present)
   - All other existing commands (stamp, commit, query, report, validate)

6. **Optional**: Add a `check-requirements` command to verify requirements-manager integration status.

The integration uses a simple approach:
- requirements-manager manages requirements (CRUD operations)
- ai-provenance reads requirements.yaml directly (no export/import)
- SPEC-IDs in git commit metadata link to requirements

See INTEGRATION_v2.md and INTEGRATION_TODO.md for complete details.

---

## Quick Reference

### Architecture
```
requirements-manager → requirements.yaml → ai-provenance reads directly
                    → .requirements-mapping.yaml (UUID → SPEC-ID)
```

### User Workflow
1. `requirements-manager add` - Create requirement
2. `requirements-manager export --format mapping` - Generate SPEC-IDs
3. `ai-prov stamp/commit --trace SPEC-001` - Link code to requirement
4. `ai-prov trace-matrix` - View traceability

### Files Changed So Far
- ✅ `src/ai_provenance/requirements.py` - New reader
- ✅ `src/ai_provenance/cli/main.py` - Removed commands
- ✅ `src/ai_provenance/reporters/traceability.py` - Reads requirements.yaml
- ⬜ `README.md` - Needs integration docs
- ⬜ `.gitignore` - Needs requirements files
- ⬜ Other files - Need import cleanup

### Testing Checklist
- [ ] No import errors when running ai-prov commands
- [ ] `ai-prov trace-matrix` reads requirements.yaml successfully
- [ ] All existing commands still work
- [ ] Documentation updated
- [ ] Old backup directory removed
- [ ] .gitignore updated

---

## Next Agent Session

Start a new Claude Code session in `/home/joe/ai/ai-provenance` and provide the "Summary Prompt for Claude Code" above. The agent will complete the integration.
