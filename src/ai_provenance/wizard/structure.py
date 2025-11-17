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

COMMAND_REQ = """# Create AI Provenance Requirement

You are helping the user create a new requirement for AI Provenance tracking.

**Instructions:**
1. Use the AskUserQuestion tool to collect the following information:
   - Requirement ID (e.g., SPEC-001, SPEC-002)
   - Title (brief summary)
   - Description (detailed description)
   - Type (feature, bug, enhancement, documentation)
   - Priority (critical, high, medium, low)

2. After collecting the information, run the ai-prov requirement create command with the collected data

3. Show the user the created requirement and ask if they want to create another one

**Example:**
```bash
ai-prov requirement create SPEC-001 \\
  --title "Hello World Program" \\
  --description "Create a simple program that greets the user" \\
  --type feature \\
  --priority high
```

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
        """Create Claude Code slash commands."""
        created = []

        commands = {
            ".claude/commands/req.md": COMMAND_REQ,
            ".claude/commands/trace.md": COMMAND_TRACE,
            ".claude/commands/stamp.md": COMMAND_STAMP,
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
            "commands": 3,
            "description": "Recommended AI-provenance project structure",
        }
