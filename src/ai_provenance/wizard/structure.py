"""
Recommended project structure and scaffolding.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
import json


# ============================================================================
# RECOMMENDED PROJECT STRUCTURE
# ============================================================================

RECOMMENDED_STRUCTURE = {
    # AI Provenance data
    ".ai-prov/": {
        "description": "AI provenance tracking data",
        "contents": {
            "requirements/": "Requirements database (SPEC-xxx.json)",
            "tests/": "Test case database (TC-xxx.json)",
            "prompts/": "Stored prompts",
            "conversations/": "Full AI conversations",
            "traces/": "Traceability links",
            "analysis/": "Project analysis results",
            "features.json": "Feature flags configuration",
        },
    },
    # Documentation
    "docs/": {
        "description": "Project documentation",
        "contents": {
            "requirements/": "Requirements documentation",
            "architecture/": "Architecture diagrams and docs",
            "api/": "API documentation",
            "guides/": "User and developer guides",
        },
    },
    # Requirements and specifications
    "specs/": {
        "description": "Formal specifications and requirements",
        "contents": {
            "features/": "Feature specifications",
            "requirements/": "Detailed requirements",
            "test-cases/": "Test case specifications",
        },
    },
    # Tests
    "tests/": {
        "description": "Test suite",
        "contents": {
            "unit/": "Unit tests",
            "integration/": "Integration tests",
            "e2e/": "End-to-end tests",
            "fixtures/": "Test fixtures and data",
        },
    },
    # Standards and conventions
    ".standards/": {
        "description": "Project standards and conventions",
        "contents": {
            "CODING_STANDARDS.md": "Coding standards and style guide",
            "TESTING_PROCEDURES.md": "Testing procedures",
            "REVIEW_CHECKLIST.md": "Code review checklist",
            "CONVENTIONS.md": "Naming and organizational conventions",
        },
    },
    # Claude Code integration
    ".claude/": {
        "description": "Claude Code configuration and commands",
        "contents": {
            "commands/": "Slash commands for Claude Code",
        },
    },
}


# ============================================================================
# TEMPLATE FILES
# ============================================================================

TEMPLATE_CODING_STANDARDS = """# Coding Standards

## General Principles

1. **Clarity over cleverness**: Write code that is easy to understand
2. **Consistency**: Follow established patterns in the codebase
3. **Documentation**: Document why, not what
4. **Testing**: Write tests for all new code
5. **AI Transparency**: Tag all AI-generated code with metadata

## Language-Specific Standards

### Python

- **Style**: Follow PEP 8
- **Line length**: 100 characters
- **Imports**: Group stdlib, third-party, local
- **Docstrings**: Google style
- **Type hints**: Use for all public functions

### JavaScript/TypeScript

- **Style**: Prettier with default config
- **Semicolons**: Always use
- **Quotes**: Single quotes
- **Async**: Prefer async/await over promises

## AI Code Standards

All AI-generated code must:

1. Include inline metadata comment:
   ```python
   # ai:tool:confidence | trace:SPEC-XXX | test:TC-YYY
   ```

2. Be reviewed by a human before merging

3. Have associated test coverage

4. Link to a requirement or feature specification

## Code Review Checklist

- [ ] Code follows project conventions
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] AI code properly tagged
- [ ] No security vulnerabilities
- [ ] Performance considered
"""

TEMPLATE_TESTING_PROCEDURES = """# Testing Procedures

## Test Pyramid

```
        /\\
       /E2E\\
      /------\\
     /  Inte- \\
    /  gration \\
   /------------\\
  /     Unit     \\
 /----------------\\
```

- **70% Unit tests**: Fast, isolated, focused
- **20% Integration tests**: Component interactions
- **10% E2E tests**: Full system workflows

## Test Categories

### Unit Tests

**Purpose**: Test individual functions/classes in isolation

**Location**: `tests/unit/`

**Naming**: `test_<module>_<function>.py`

**Example**:
```python
# tests/unit/test_auth_jwt.py

def test_generate_jwt_token():
    \"\"\"Test JWT token generation.\"\"\"
    token = generate_jwt("user123")
    assert validate_jwt(token) == "user123"
```

### Integration Tests

**Purpose**: Test component interactions

**Location**: `tests/integration/`

**Requirements**: May need database, external services

### E2E Tests

**Purpose**: Test full user workflows

**Location**: `tests/e2e/`

**Requirements**: Full system running

## Running Tests

```bash
# All tests
pytest

# Specific category
pytest tests/unit/
pytest tests/integration/

# With coverage
pytest --cov=src --cov-report=html

# AI provenance validation
ai-prov validate --require-tests
```

## Test Case Documentation

Every test should:

1. Have a clear name describing what it tests
2. Include a docstring explaining the test
3. Be linked to a requirement (via `# trace:SPEC-XXX`)
4. Test one thing (single responsibility)

## AI-Generated Tests

Tests generated by AI should:

1. Be tagged with AI metadata
2. Be reviewed for correctness and completeness
3. Include edge cases, not just happy path
4. Link to the requirement they verify

Example:
```python
# ai:claude:high | trace:SPEC-089 | test:TC-210

def test_jwt_expiration():
    \"\"\"Test that JWT tokens expire correctly.\"\"\"
    # AI-generated test for JWT expiration
    token = generate_jwt("user123", exp_minutes=1)

    # Token should be valid immediately
    assert validate_jwt(token) == "user123"

    # Simulate time passing (mock time)
    with freeze_time(datetime.now() + timedelta(minutes=2)):
        with pytest.raises(ExpiredTokenError):
            validate_jwt(token)
```

## Continuous Integration

All tests must pass before merging:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: pytest --cov --cov-fail-under=80
      - name: Validate AI provenance
        run: ai-prov validate --require-tests
```

## Coverage Requirements

- **Overall**: Minimum 80% coverage
- **New code**: Minimum 90% coverage
- **Critical paths**: 100% coverage
- **AI-generated code**: 95% coverage (extra scrutiny)
"""

TEMPLATE_CONVENTIONS = """# Project Conventions

## File Organization

```
project/
├── src/                    # Source code
│   └── package_name/       # Main package
├── tests/                  # Test suite
├── docs/                   # Documentation
├── specs/                  # Specifications
├── .ai-prov/               # AI provenance data
└── .standards/             # Standards documentation
```

## Naming Conventions

### Files and Directories

- **Modules**: `snake_case.py`
- **Packages**: `snake_case/`
- **Tests**: `test_<module>.py`
- **Docs**: `kebab-case.md`

### Code (Python)

- **Variables**: `snake_case`
- **Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`

### Code (JavaScript/TypeScript)

- **Variables**: `camelCase`
- **Functions**: `camelCase`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `#private` (ES2022)

## Requirements and Features

### Requirement IDs

Format: `<TYPE>-<NUMBER>`

Types:
- `SPEC-XXX`: Specification/requirement
- `FEAT-XXX`: Feature
- `BUG-XXX`: Bug fix
- `ENH-XXX`: Enhancement
- `DOC-XXX`: Documentation

Example: `SPEC-089`, `FEAT-042`

### Test Case IDs

Format: `TC-<NUMBER>`

Example: `TC-210`, `TC-001`

## Commit Messages

Use conventional commits with AI provenance:

```
[AI:tool:confidence] type(scope): subject

Body (optional)

Trace: SPEC-XXX, FEAT-YYY
Test: TC-ZZZ
Reviewed-by: AI+user@example.com
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance

## Branch Naming

- `feature/SPEC-XXX-description`
- `bugfix/BUG-XXX-description`
- `hotfix/critical-description`
- `docs/update-description`

## Pull Request Template

```markdown
## Description
Brief description of changes

## Type
- [ ] Feature
- [ ] Bug fix
- [ ] Enhancement
- [ ] Documentation

## Requirements
Closes: SPEC-XXX, FEAT-YYY

## AI Code
- AI tool used: Claude/Copilot/etc
- AI confidence: high/med/low
- % AI-generated: XX%

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] AI code tagged
- [ ] Linked to requirements
- [ ] Code reviewed
```

## Documentation

### Docstrings (Python)

Use Google style:

```python
def function(arg1: str, arg2: int) -> bool:
    \"\"\"Brief description.

    Longer description if needed.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: When arg2 is negative
    \"\"\"
```

### Comments

- Use comments to explain WHY, not WHAT
- Keep comments up to date
- Tag AI code with metadata comments

```python
# ai:claude:high | trace:SPEC-089 | test:TC-210
# This function was AI-generated with high confidence
def complex_algorithm():
    # Explain the approach, not the code
    pass
```

## Error Handling

- Use specific exceptions
- Provide helpful error messages
- Log errors appropriately
- Don't catch generic `Exception` unless necessary

## Configuration

- Store config in environment variables or config files
- Never commit secrets or credentials
- Use `.env.example` for documentation
- Validate configuration on startup
"""

TEMPLATE_REVIEW_CHECKLIST = """# Code Review Checklist

## General

- [ ] Code follows project coding standards
- [ ] Code is self-documenting and clear
- [ ] No commented-out code (unless with explanation)
- [ ] No debug statements left in code
- [ ] Error handling is appropriate

## AI Code Specific

- [ ] All AI-generated code has inline metadata tags
- [ ] AI confidence level is appropriate
- [ ] Human review completed and documented
- [ ] AI-generated code links to requirements
- [ ] Tests exist for AI-generated code

## Functionality

- [ ] Code does what it's supposed to do
- [ ] Edge cases are handled
- [ ] Error cases are handled
- [ ] No obvious bugs
- [ ] Performance is acceptable

## Testing

- [ ] New tests added for new functionality
- [ ] Existing tests still pass
- [ ] Test coverage is adequate (>80%)
- [ ] Tests are meaningful and test the right things
- [ ] AI-generated tests reviewed for correctness

## Documentation

- [ ] Public APIs are documented
- [ ] Complex logic is explained
- [ ] README updated if needed
- [ ] REQUIREMENTS.md updated if needed
- [ ] CHANGELOG updated

## Security

- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] No hard-coded credentials
- [ ] Input validation is present
- [ ] Sensitive data is properly handled

## Requirements Traceability

- [ ] Code links to requirements (SPEC-XXX)
- [ ] Requirements are implemented correctly
- [ ] All acceptance criteria met
- [ ] Test cases cover requirements
- [ ] Traceability matrix updated

## Git & Version Control

- [ ] Commit messages are clear
- [ ] Commits are logical and atomic
- [ ] Branch name follows convention
- [ ] No merge conflicts
- [ ] AI provenance metadata in commits

## Before Merge

- [ ] All CI checks passing
- [ ] Code review approved
- [ ] AI provenance validation passed
- [ ] No unresolved comments
- [ ] Branch is up to date with main
"""

# ============================================================================
# CLAUDE CODE SLASH COMMANDS
# ============================================================================

COMMAND_REQ = """# Create Requirement with requirements-manager

You are helping the user create a new requirement using requirements-manager.

**Instructions:**
1. Use the AskUserQuestion tool to collect the following information:
   - Title (brief summary)
   - Description (detailed description)
   - Feature name (e.g., Authentication, Core, UI)
   - Priority (Critical, High, Medium, Low)
   - Status (Draft, InProgress, Completed, Verified)

2. After collecting the information, run the requirements-manager add command
   - This creates the requirement in requirements.yaml
   - It automatically generates a UUID and assigns a SPEC-ID

3. Then run requirements-manager export to update the mapping:
   ```bash
   requirements-manager export --format mapping
   ```

4. Show the user the created requirement (with SPEC-ID) and ask if they want to create another one

**Example:**
```bash
# Create requirement
requirements-manager add \\
  --title "Hello World Program" \\
  --description "Create a simple program that greets the user" \\
  --feature Core \\
  --priority High \\
  --status Draft

# Output: Created requirement with UUID abc-123... (SPEC-001)

# Update mapping file
requirements-manager export --format mapping

# Output: ✓ Generated mapping file: .requirements-mapping.yaml
```

**Notes:**
- requirements-manager is the ONLY way to create requirements
- SPEC-IDs are auto-generated from UUIDs
- The mapping file (.requirements-mapping.yaml) links UUIDs to SPEC-IDs
- ai-provenance reads directly from requirements.yaml for traceability

Be friendly and guide the user through the process step by step.
"""

COMMAND_TRACE = """# Link Code to Requirement

You are helping the user link code to a requirement for traceability.

**Instructions:**
1. Use the AskUserQuestion tool to collect:
   - Requirement ID to link to
   - What to link (file, commit, or test)
   - The path/ID to link

2. Run the appropriate ai-prov requirement link command

3. Confirm the link was created successfully

**Example:**
```bash
ai-prov requirement link SPEC-001 --file src/hello.py
ai-prov requirement link SPEC-001 --commit abc123
ai-prov requirement link SPEC-001 --test TC-001
```

Be helpful and confirm the traceability link was established.
"""

COMMAND_STAMP = """# Stamp AI Metadata on Code

You are helping the user add AI provenance metadata to a code file.

**Instructions:**
1. Use the AskUserQuestion tool to collect:
   - File path to stamp
   - AI tool used (claude, copilot, chatgpt, etc.)
   - Confidence level (high, med, low)
   - Optional: Requirement IDs (trace)
   - Optional: Test case IDs (test)
   - Optional: Reviewer email

2. Run the ai-prov stamp command with the collected data

3. Show the user the stamped file and confirm success

**Example:**
```bash
ai-prov stamp src/auth.py \\
  --tool claude \\
  --conf high \\
  --trace SPEC-089 \\
  --test TC-210 \\
  --reviewer alice@example.com
```

Guide the user through adding provenance metadata to their AI-generated code.
"""

COMMAND_IMPLEMENT = """# Implement AI Provenance Requirement

You are helping the user implement a requirement following AI provenance best practices.

**Instructions:**

1. **Ask which requirement to implement:**
   - Use AskUserQuestion to get the requirement ID (e.g., SPEC-001)
   - Or ask if they want to see the list first

2. **Read the requirement:**
   - Run: `requirements-manager show <SPEC_ID>` to see full requirement details
   - Parse the requirement details (title, description, feature, priority, status)
   - Note: SPEC-IDs are in the mapping file (.requirements-mapping.yaml)

3. **Create an implementation plan:**
   - Based on the requirement, propose:
     - Source files to create
     - Test files to create
     - Documentation to add
   - Show the plan to the user and get approval

4. **Implement the code:**
   - Create ALL files with AI provenance tags at the top:
     - Source files: `# ai:claude:high | trace:SPEC-XXX`
     - Supporting files (.gitignore, __init__.py, etc.): same tags
     - IMPORTANT: Every file you create must be tagged, not just main files
   - Write clean, documented code
   - Use type hints (Python) or proper typing (other languages)
   - Follow coding standards from `.standards/CODING_STANDARDS.md` if present

5. **Create comprehensive tests:**
   - Create test files with:
     - AI provenance tags: `# ai:claude:high | trace:SPEC-XXX | test:TC-XXX`
     - Unit tests covering happy path and edge cases
     - Clear test names and docstrings
   - Place in appropriate test directory (tests/unit/, tests/integration/)

6. **Link via git commit:**
   - Linking happens automatically via commit metadata
   - The Trace: SPEC-XXX in commit messages creates the traceability link
   - No separate link command needed (requirements-manager integration)

7. **Commit with provenance:**
   - Stage all created files
   - Create commit with proper format:
     ```
     [AI:claude:high] <type>: <subject>

     <body>

     Trace: SPEC-XXX
     Test: TC-XXX
     ```

8. **Show summary:**
   - List files created
   - Show requirement status
   - Suggest next steps (run tests, create another requirement, etc.)

**Best Practices to Follow:**

- **Traceability**: Every file must link back to a requirement
- **Testing**: Write tests before or alongside implementation
- **Documentation**: Add docstrings and comments explaining WHY, not WHAT
- **AI Transparency**: Tag all AI-generated code with provenance metadata
- **Atomic commits**: One requirement per commit when possible

**Example Workflow:**

```bash
# Read requirement from requirements-manager
requirements-manager show SPEC-001

# Create implementation files (you do this with Write tool)
# src/hello.py with proper tags: # ai:claude:high | trace:SPEC-001

# Commit with traceability (this creates the link)
git add src/hello.py tests/unit/test_hello.py
git commit -m "[AI:claude:high] feat: implement hello world greeting

Implemented greeting function per SPEC-001.

Trace: SPEC-001
Test: TC-001"

# Optionally update requirement status in requirements-manager
requirements-manager edit <uuid> --status Completed
```

**Important Notes:**

- Always read the requirement first to understand what to build
- Ask clarifying questions if the requirement is unclear
- Create tests that verify all acceptance criteria
- Use the TodoWrite tool to track implementation steps
- Be thorough and follow all best practices from `.standards/`

Guide the user through each step and ensure they understand the provenance workflow.
"""

COMMAND_DOC = """# Generate and Manage Documentation

You are helping the user with documentation tasks for their project.

**Use the AskUserQuestion tool to ask what documentation task they need.**

## Available Documentation Tasks

### 1. Generate HTML Documentation
Generate HTML versions of Markdown documentation.

**Command:**
```bash
python helper/generate_docs.py
```

This converts README.md and other docs to HTML with light/dark mode CSS.

### 2. Update README.md
Update README with latest features from CLAUDE.md.

### 3. Update CLAUDE.md
Update project context with recent changes and new features.

### 4. Generate Changelog
Create CHANGELOG.md from git commit history.

## Workflow

1. Ask which documentation task
2. Execute the appropriate action
3. Show what was generated
4. Ask if they want to commit changes

Be helpful and guide the user through documentation!
"""

COMMAND_RELEASE = """# Release Readiness Check

You are helping the user determine if it's time to create a new release.

## Step 1: Check Recent Activity

First, check if there have been any commits in the last 7 days:

```bash
git log --since="7 days ago" --oneline | wc -l
```

**If count is 0**: Stop and report "No commits in the last 7 days. No release needed."

## Step 2: Find Latest Tag

```bash
# Get latest tag
latest_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

# If no tags exist
if [ -z "$latest_tag" ]; then
    echo "No tags found - recommend initial v0.1.0 release"
else
    # Get tag date
    git log -1 --format=%ai $latest_tag
fi
```

## Step 3: Calculate Changes Since Last Tag

```bash
# Lines changed since tag (or since first commit if no tags)
if [ -n "$latest_tag" ]; then
    git diff --stat $latest_tag..HEAD | tail -1
else
    git diff --stat $(git rev-list --max-parents=0 HEAD)..HEAD | tail -1
fi
```

Parse the output to extract:
- Files changed
- Lines added (insertions)
- Lines removed (deletions)

## Step 4: Calculate Days Since Last Tag

```bash
if [ -n "$latest_tag" ]; then
    tag_date=$(git log -1 --format=%ct $latest_tag)
    current_date=$(date +%s)
    days_since=$((($current_date - $tag_date) / 86400))
    echo "Days since last tag: $days_since"
fi
```

## Step 5: Run tokei for Current Statistics

```bash
tokei --output json
```

If tokei is not installed, skip this step and note it in the report.

## Step 6: Evaluate Thresholds

Calculate total lines changed = insertions + deletions

**Thresholds:**
- Lines changed: > 3000 lines
- Days since tag: > 7 days
- Recent activity: At least 1 commit in last 7 days (required)

**Default behavior:**
- If EITHER threshold exceeded AND recent activity: **Recommend release (default: YES)**
- If neither threshold met BUT recent activity exists: **Ask user (default: NO)**
- If no recent activity: **No release**

## Step 7: Suggest Version Number

Analyze commit messages since last tag to determine version bump:

```bash
# Get commit messages since last tag
if [ -n "$latest_tag" ]; then
    git log $latest_tag..HEAD --format=%s
else
    git log --format=%s
fi
```

**Version bump logic:**
1. Look for keywords in commit messages:
   - **Major**: "BREAKING CHANGE", "breaking:", "major:"
   - **Minor**: "feat:", "feature:", "minor:"
   - **Patch**: "fix:", "patch:", "chore:", "docs:", or default

2. If current tag is v0.x.x, suggest bumping minor (pre-1.0 development)
3. If no tag exists, suggest v0.1.0

**Examples:**
- v1.2.3 + patch → v1.2.4
- v1.2.3 + minor → v1.3.0
- v1.2.3 + major → v2.0.0
- v0.5.0 + any → v0.6.0 (pre-1.0)
- (no tag) → v0.1.0

## Step 8: Generate Summary Report

Display a well-formatted report:

```
===============================================
Release Readiness Check
===============================================

Last Release:
  Tag: v1.2.3 (or "None - initial release")
  Date: 2025-11-16 14:23:45 -0500
  Days ago: 10

Changes Since Last Release:
  Files changed: 45
  Lines added: 2,345
  Lines removed: 891
  Total changed: 3,236 lines

Recent Activity:
  Commits in last 7 days: 15

Current Codebase (tokei):
  Total lines: 15,234
  Code: 12,456
  Comments: 1,890
  Blanks: 888

Threshold Evaluation:
  ✓ Lines changed: 3,236 > 3,000 (EXCEEDED)
  ✓ Days since release: 10 > 7 (EXCEEDED)
  ✓ Recent activity: 15 commits (ACTIVE)

Version Suggestion:
  Current: v1.2.3
  Recommended: v1.3.0 (minor bump - new features detected)

  Detected changes:
  - 8 feat: commits (new features)
  - 5 fix: commits (bug fixes)
  - 2 chore: commits (maintenance)

Recommendation: CREATE RELEASE NOW (default)
===============================================
```

## Step 9: Prompt User for Action

Use the AskUserQuestion tool to ask:

**Question**: "Create release now?"

**Options based on thresholds:**

If thresholds exceeded (default: YES):
- "Yes, create v1.3.0 now" (default)
- "No, not yet"

If thresholds not met (default: NO):
- "Yes, create v1.3.0 anyway"
- "No, wait for more changes" (default)

**Note**: In automated mode, the default is selected automatically.

## Step 10: If User Chooses Yes

Guide them through release creation:

1. **Ask for release notes** (optional):
   ```
   What should the release notes include?
   - Auto-generate from commits
   - I'll provide custom notes
   - Skip release notes
   ```

2. **Create the tag**:
   ```bash
   git tag -a v1.3.0 -m "Release v1.3.0

   [Release notes here]
   "
   ```

3. **Push the tag**:
   ```bash
   git push origin v1.3.0
   ```

4. **Optional**: Guide creation of GitHub release
   ```bash
   gh release create v1.3.0 --generate-notes
   # or
   gh release create v1.3.0 --notes "Custom notes"
   ```

## Important Notes

- Always check recent activity first (commits in last 7 days)
- Thresholds determine DEFAULT behavior, not absolute rules
- User can always override and create release anyway
- In automated CI/CD, default behavior is used
- Suggest appropriate version bump based on commit messages
- Handle "no tags" case by recommending v0.1.0

## Error Handling

- If not in a git repository: Error and exit
- If tokei not found: Continue without tokei statistics
- If gh CLI not found: Skip GitHub release creation step
- If no commits ever: "Nothing to release"
"""


class ProjectScaffolder:
    """Create recommended project structure."""

    def __init__(self, repo_path: Optional[str] = None):
        """Initialize scaffolder."""
        if repo_path is None:
            repo_path = "."

        self.repo_path = Path(repo_path)

    def create_structure(self, dry_run: bool = False) -> List[str]:
        """Create recommended directory structure."""
        created = []

        for dir_name, config in RECOMMENDED_STRUCTURE.items():
            dir_path = self.repo_path / dir_name

            if not dry_run:
                dir_path.mkdir(exist_ok=True)

            created.append(f"Created directory: {dir_name}")

            # Create subdirectories
            if "contents" in config and isinstance(config["contents"], dict):
                for subdir in config["contents"]:
                    if subdir.endswith("/"):
                        subdir_path = dir_path / subdir
                        if not dry_run:
                            subdir_path.mkdir(exist_ok=True)
                        created.append(f"  Created subdirectory: {dir_name}{subdir}")

        return created

    def create_standards_templates(self, dry_run: bool = False) -> List[str]:
        """Create standard template files."""
        created = []

        templates = {
            ".standards/CODING_STANDARDS.md": TEMPLATE_CODING_STANDARDS,
            ".standards/TESTING_PROCEDURES.md": TEMPLATE_TESTING_PROCEDURES,
            ".standards/CONVENTIONS.md": TEMPLATE_CONVENTIONS,
            ".standards/REVIEW_CHECKLIST.md": TEMPLATE_REVIEW_CHECKLIST,
        }

        for file_path, content in templates.items():
            full_path = self.repo_path / file_path

            if not dry_run:
                full_path.parent.mkdir(exist_ok=True)
                full_path.write_text(content)

            created.append(f"Created template: {file_path}")

        return created

    def create_readme_template(self, project_name: str, dry_run: bool = False) -> str:
        """Create or update README with AI provenance section."""
        readme_addition = f"""

## AI Provenance

This project uses [ai-provenance](https://github.com/ai-provenance/ai-provenance) to track AI-generated code.

### Quick Stats

```bash
# Check AI contribution
ai-prov query --ai-percent

# View requirements
ai-prov requirement list

# Generate traceability matrix
ai-prov trace-matrix
```

### For Developers

All AI-generated code is tagged with metadata:

```python
# ai:claude:high | trace:SPEC-089 | test:TC-210
def ai_generated_function():
    pass
```

See `.standards/` for coding standards and conventions.
"""

        if not dry_run:
            readme_path = self.repo_path / "README.md"

            if readme_path.exists():
                content = readme_path.read_text()
                if "## AI Provenance" not in content:
                    readme_path.write_text(content + readme_addition)
            else:
                readme_path.write_text(f"# {project_name}\n{readme_addition}")

        return readme_addition

    def create_claude_commands(self, dry_run: bool = False) -> List[str]:
        """Create Claude Code slash commands with /ap- prefix."""
        created = []

        commands = {
            ".claude/commands/ap-req.md": COMMAND_REQ,
            ".claude/commands/ap-implement.md": COMMAND_IMPLEMENT,
            ".claude/commands/ap-trace.md": COMMAND_TRACE,
            ".claude/commands/ap-stamp.md": COMMAND_STAMP,
            ".claude/commands/ap-doc.md": COMMAND_DOC,
            ".claude/commands/ap-release.md": COMMAND_RELEASE,
        }

        for file_path, content in commands.items():
            full_path = self.repo_path / file_path

            if not dry_run:
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content)

            created.append(f"Created command: {file_path}")

        return created

    def get_structure_summary(self) -> Dict[str, Any]:
        """Get summary of recommended structure."""
        return {
            "directories": list(RECOMMENDED_STRUCTURE.keys()),
            "total_dirs": sum(
                1
                + len([k for k in v.get("contents", {}) if k.endswith("/")])
                for v in RECOMMENDED_STRUCTURE.values()
            ),
            "templates": 4,
            "commands": 5,
            "description": "Recommended AI-provenance project structure",
        }
