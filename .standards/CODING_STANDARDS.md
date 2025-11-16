# AI Provenance - Coding Standards

## General Principles

1. **Clarity over cleverness**: Write code that is easy to understand
2. **Consistency**: Follow established patterns in the codebase
3. **Documentation**: Document why, not what
4. **Testing**: Write tests for all new code
5. **AI Transparency**: Tag all AI-generated code with metadata

## Python Standards

- **Style**: Follow PEP 8
- **Line length**: 100 characters
- **Imports**: Group stdlib, third-party, local with blank lines
- **Docstrings**: Google style for all public functions/classes
- **Type hints**: Required for all public APIs

### Example

```python
from typing import Optional


def calculate_ai_percentage(total_lines: int, ai_lines: int) -> float:
    """Calculate percentage of AI-generated code.

    Args:
        total_lines: Total number of lines in the file
        ai_lines: Number of AI-generated lines

    Returns:
        Percentage as a float (0-100)

    Raises:
        ValueError: If total_lines is zero or negative
    """
    if total_lines <= 0:
        raise ValueError("total_lines must be positive")

    return (ai_lines / total_lines) * 100
```

## AI Code Standards

**ALL AI-generated code MUST include inline metadata:**

```python
# ai:claude:high | trace:SPEC-001 | test:TC-001 | reviewed:2025-11-16:joe
def ai_generated_function():
    """AI-generated function with metadata tag."""
    pass
```

**Confidence Levels:**
- `high` (>80% AI): Largely copy-pasted from AI with minor edits
- `med` (40-80% AI): Significant human modifications
- `low` (<40% AI): Mostly human-written, AI-assisted

## Code Review Requirements

All AI-generated code must:
1. Include metadata tag
2. Be reviewed by a human
3. Have associated test coverage
4. Link to a requirement (SPEC-xxx) or feature (FEAT-xxx)

## Testing Standards

- Minimum 80% overall coverage
- 90% coverage for new code
- 95% coverage for AI-generated code (extra scrutiny)
- All public APIs must have tests

## Documentation Standards

- All modules have module docstrings
- All public functions/classes have docstrings
- Complex algorithms explained in comments
- AI code explains the approach, not just the implementation
