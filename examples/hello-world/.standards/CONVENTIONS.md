# Project Conventions

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
    """Brief description.

    Longer description if needed.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: When arg2 is negative
    """
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
