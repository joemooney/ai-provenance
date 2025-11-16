# AI Provenance

**Git-native AI code provenance and metadata tracking system**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview

`ai-provenance` is a comprehensive, language-agnostic tool for tracking, attributing, and auditing AI-generated code. It provides hierarchical metadata management (line → block → function → file level) using Git-native mechanisms with full temporal coverage.

## Features

- 🏷️ **Hierarchical Metadata**: Track AI contributions at line, block, function, and file levels
- 📝 **Commit Convention**: Structured, machine-parsable commit messages with AI attribution
- 📊 **Git Notes**: Rich metadata stored in Git notes for immutable provenance
- 🔍 **Temporal Coverage**: Reconstruct metadata for any historical version
- 🔗 **Traceability**: Link code to requirements (SPEC-xxx) and test cases (TC-xxx)
- ✅ **Review Tracking**: Record human review of AI-generated code
- 📈 **Reporting**: Generate comprehensive reports and metrics
- 🔧 **Language Agnostic**: Works with any text-based programming language
- 🚀 **CI/CD Integration**: Ready-to-use GitHub Actions and GitLab CI templates
- 📦 **Zero Dependencies**: All data stored in Git repo, no external databases

## Quick Start

### Installation

```bash
pip install ai-provenance
```

### Initialize Repository

```bash
cd your-project
ai-prov init
```

This sets up:
- Git hooks for automatic metadata tracking
- Filter driver for `.meta.json` generation
- Git notes namespace for provenance data

### Stamp Code with AI Metadata

```bash
# Add inline metadata to a file
ai-prov stamp src/auth.py --tool claude --conf high \
  --trace SPEC-89 --test TC-210 --reviewer alice@example.com
```

### Commit with Provenance

```bash
# Structured commit with full metadata
ai-prov commit -m "feat(auth): add JWT refresh endpoint" \
  --tool claude --conf high \
  --trace SPEC-89 --test TC-210,TC-211
```

This generates a commit message:
```
[AI:claude:high] feat(auth): add JWT refresh endpoint
Trace: SPEC-89
Test: TC-210, TC-211
Reviewed-by: AI+alice@example.com
```

### Generate Reports

```bash
# File-level report with full history
ai-prov report src/auth.py

# Repository-wide metrics
ai-prov query --ai-percent --by-file

# Find unreviewed AI code
ai-prov query --unreviewed

# Traceability matrix
ai-prov trace-matrix > TRACEABILITY.md
```

## Metadata Schema

`ai-provenance` tracks metadata at multiple levels:

### Commit Level (Git Notes)
```json
{
  "ai_tool": "claude",
  "confidence": "high",
  "trace": ["SPEC-89"],
  "tests": ["TC-210"],
  "reviewed_by": "alice@example.com",
  "reviewed_at": "2025-11-16T14:00:00Z"
}
```

### File Level (`.meta.json`)
```json
{
  "file": "src/auth.py",
  "generated_at": "2025-11-16T13:38:00Z",
  "ai_tool": "claude",
  "confidence": "high",
  "trace": ["SPEC-89"],
  "tests": ["TC-210", "TC-211"],
  "reviewed_by": "alice@example.com",
  "blocks": [
    {
      "kind": "function",
      "name": "refresh_token",
      "lines": [42, 68],
      "ai": true,
      "confidence": "high"
    }
  ]
}
```

### Line Level (Inline Comments)
```python
# ai:claude:high | trace:SPEC-89 | test:TC-210 | reviewed:2025-11-16:alice
def refresh_token(token: str) -> str:
    # AI-generated implementation
    ...
```

## Commands

### `ai-prov init`
Initialize provenance tracking in a repository.

### `ai-prov stamp <file>`
Add AI metadata inline comments to a file.

**Options:**
- `--tool`: AI tool used (claude, copilot, chatgpt, etc.)
- `--conf`: Confidence level (high, med, low)
- `--trace`: Requirements/specs (SPEC-123)
- `--test`: Test cases (TC-456)
- `--reviewer`: Human reviewer email

### `ai-prov commit`
Create a commit with structured provenance metadata.

### `ai-prov report <file> [--rev <commit>]`
Generate a comprehensive metadata report for a file.

### `ai-prov query`
Query repository for AI code metrics.

**Options:**
- `--ai-percent`: Show % of AI-generated code
- `--by-file`: Break down by file
- `--unreviewed`: Find unreviewed AI code
- `--trace <spec>`: Find code for a requirement

### `ai-prov validate`
Validate repository metadata integrity.

**Options:**
- `--require-review`: Ensure all AI code is reviewed
- `--require-tests`: Ensure all traced code has tests

### `ai-prov trace-matrix`
Generate a traceability matrix (features → code → tests).

## CI/CD Integration

### GitHub Actions

```yaml
name: AI Provenance Check
on: [pull_request]

jobs:
  provenance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }

      - name: Install ai-provenance
        run: pip install ai-provenance

      - name: Validate AI metadata
        run: ai-prov validate --require-review --require-tests

      - name: Generate PR comment
        run: ai-prov report --pr-comment >> $GITHUB_STEP_SUMMARY
```

### GitLab CI

```yaml
ai-provenance:
  stage: test
  script:
    - pip install ai-provenance
    - ai-prov validate --require-review
    - ai-prov query --ai-percent > metrics.txt
  artifacts:
    reports:
      dotenv: metrics.txt
```

## Architecture

```
ai-provenance/
├── src/ai_provenance/
│   ├── cli/          # Command-line interface
│   ├── core/         # Core metadata models and schemas
│   ├── git_integration/ # Git hooks, filters, and notes
│   ├── parsers/      # Language-agnostic code parsers
│   ├── reporters/    # Report generation
│   └── ci_templates/ # CI/CD templates
├── hooks/            # Git hook templates
├── tests/            # Test suite
├── examples/         # Example repositories
└── docs/             # Documentation
```

## Best Practices

1. **Tag All AI Code**: Use `ai-prov stamp` or inline comments for all AI-generated code
2. **Review Required**: Always have human review (`Reviewed-by: AI+<email>`)
3. **Link to Requirements**: Use `Trace: SPEC-xxx` for traceability
4. **Test Coverage**: Use `Test: TC-xxx` and ensure tests exist
5. **Confidence Levels**:
   - `high`: Copy-pasted with minor edits
   - `med`: Significant modifications
   - `low`: AI-assisted but mostly human-written
6. **Commit Conventions**: Follow structured format for machine parsing
7. **CI Validation**: Run `ai-prov validate` in CI/CD pipeline

## Development

### Setup

```bash
git clone https://github.com/ai-provenance/ai-provenance
cd ai-provenance
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Format Code

```bash
black src tests
ruff check src tests
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Support

- 📚 [Documentation](https://ai-provenance.readthedocs.io)
- 🐛 [Issue Tracker](https://github.com/ai-provenance/ai-provenance/issues)
- 💬 [Discussions](https://github.com/ai-provenance/ai-provenance/discussions)
