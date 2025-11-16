# AI Provenance - Project Conventions

## Requirement IDs

Format: `<TYPE>-<NUMBER>`

**Types:**
- `SPEC-XXX`: Core specification/requirement
- `FEAT-XXX`: Feature implementation
- `BUG-XXX`: Bug fix
- `ENH-XXX`: Enhancement
- `DOC-XXX`: Documentation task

**Examples:**
- `SPEC-001`: Core metadata tracking
- `FEAT-042`: Web dashboard
- `BUG-015`: Fix git notes push issue

## Test Case IDs

Format: `TC-<NUMBER>`

**Examples:**
- `TC-001`: Test metadata parsing
- `TC-210`: Test JWT generation

## Commit Message Format

```
[AI:tool:confidence] type(scope): subject

Body (optional)

Trace: SPEC-XXX, FEAT-YYY
Test: TC-ZZZ
Reviewed-by: AI+email@example.com

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**
```
[AI:claude:high] feat(requirements): add requirements management system

Trace: SPEC-002, FEAT-010
Test: TC-050
Reviewed-by: AI+joe@example.com
```

## File Naming

- Python modules: `snake_case.py`
- Test files: `test_<module>.py`
- Markdown docs: `UPPER_CASE.md` or `kebab-case.md`

## Directory Structure

```
ai-provenance/
├── src/ai_provenance/     # Source code
├── tests/                 # Test suite
├── docs/                  # Documentation
├── specs/                 # Specifications
├── .ai-prov/              # AI provenance data
├── .standards/            # Standards docs
└── .claude/               # Claude Code integration
```

## Branch Naming

- `feature/SPEC-XXX-description`
- `bugfix/BUG-XXX-description`
- `docs/update-description`

## Module Organization

Each module should have:
- `__init__.py` with `__all__` exports
- Clear separation of concerns
- Pydantic models in `models.py`
- CLI commands in `cli/`
- Core logic separate from CLI

## Import Organization

```python
# Standard library
import json
from pathlib import Path
from typing import List, Optional

# Third-party
import click
from pydantic import BaseModel

# Local
from ai_provenance.core.models import Requirement
```
