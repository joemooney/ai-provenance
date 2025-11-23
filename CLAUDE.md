# AI Provenance - Project Context for Claude

## High-Level Feature Summary

AI Provenance is a Git-native tool for tracking, attributing, and auditing AI-generated code. It provides:

- **Hierarchical metadata tracking**: Line → block → function → file level
- **Commit message conventions**: Machine-parsable AI attribution
- **Git notes integration**: Immutable metadata storage
- **Inline code tagging**: Language-agnostic comment-based metadata
- **Reporting & querying**: Comprehensive metrics and traceability
- **CI/CD integration**: Ready-to-use GitHub Actions & GitLab CI templates

## Architecture Overview

```
ai-provenance/
├── src/ai_provenance/
│   ├── core/               # Data models (Pydantic)
│   │   └── models.py       # AITool, Confidence, FileMetadata, etc.
│   ├── cli/                # Click-based CLI
│   │   └── main.py         # Commands: init, stamp, commit, report, query
│   ├── git_integration/    # Git operations
│   │   ├── init.py         # Repository initialization
│   │   ├── commit.py       # Provenance commits
│   │   └── notes.py        # Git notes CRUD
│   ├── parsers/            # Code parsing
│   │   └── stamper.py      # Inline metadata stamping
│   ├── reporters/          # Report generation
│   │   ├── file_report.py  # File-level reports
│   │   ├── query.py        # Repository queries
│   │   ├── validator.py    # Validation logic
│   │   └── traceability.py # Trace matrices
│   └── ci_templates/       # CI/CD templates
├── hooks/                  # Git hook templates
├── tests/                  # Pytest test suite
└── examples/               # Sample projects
```

## Key Design Principles

1. **Git-native**: All metadata stored in Git (notes, commits, inline comments)
2. **Language-agnostic**: Works with any text-based code via comment patterns
3. **Zero external dependencies**: No databases, SaaS, or external services
4. **Temporal coverage**: Full historical metadata reconstruction
5. **Traceability**: Link code → requirements → tests
6. **Immutable provenance**: Git notes provide tamper-proof audit trail

## Core Components

### 1. Data Models (`core/models.py`)

- `AITool`: Enum for AI tools (claude, copilot, chatgpt, etc.)
- `Confidence`: Enum for confidence levels (high, med, low)
- `BlockMetadata`: Code block metadata (function, class, method)
- `FileMetadata`: File-level metadata with AI % calculation
- `CommitMetadata`: Git note payload
- `InlineMetadata`: Parser for inline comments
- `CommitMessage`: Parser for commit messages

### 2. CLI Commands (`cli/main.py`)

- `ai-prov init`: Initialize repo (hooks, filters, git notes)
- `ai-prov stamp`: Add inline metadata to files
- `ai-prov commit`: Create commit with provenance
- `ai-prov report`: Generate file/repo reports
- `ai-prov query`: Query AI %, unreviewed code, traces
- `ai-prov validate`: Validate metadata integrity
- `ai-prov trace-matrix`: Generate traceability matrix

### 3. Git Integration

- **Hooks**: commit-msg, post-commit, pre-push
- **Notes**: Namespace `ai-provenance` for commit metadata
- **Filters**: (Planned) Auto-generate .meta.json on staging

### 4. Inline Metadata Format

```python
# ai:tool:conf | trace:SPEC-xxx | test:TC-xxx | reviewed:YYYY-MM-DD:name
```

Language-agnostic patterns for #, //, /*, --, etc.

### 5. Commit Message Convention

```
[AI:tool:conf] type(scope): subject
Trace: SPEC-xxx, SPEC-yyy
Test: TC-aaa, TC-bbb
Reviewed-by: AI+user@example.com
```

## Recent Major Updates

### Session 1 (2025-11-16)

- Initial project structure and architecture
- Core data models with Pydantic validation
- CLI framework with Click
- Git integration (init, commit, notes)
- Inline metadata parsing and stamping
- Reporters (file reports, queries, validation, traceability)
- Git hooks (commit-msg, post-commit, pre-push)
- CI/CD templates (GitHub Actions, GitLab CI)
- Documentation and examples
- Test suite foundation

## Technical Limitations

1. **Filter driver not implemented**: .meta.json auto-generation is stubbed
2. **Hunk detection heuristic**: `_find_hunk_end()` uses simple rules
3. **No tree-sitter integration**: Function/class detection is basic
4. **Line-level tracking**: Currently counts metadata lines, not actual AI lines
5. **No diff analysis**: Can't track AI % changes over time yet
6. **Git notes push**: Requires manual push or pre-push hook

## Common Commands

### Setup
```bash
cd /home/joe/ai/ai-provenance
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### Development
```bash
pytest                          # Run tests
black src tests                 # Format code
ruff check src tests           # Lint code
ai-prov --help                 # CLI help
```

### Usage
```bash
ai-prov init                   # Initialize repo
ai-prov stamp file.py --tool claude --conf high --trace SPEC-123
ai-prov commit -m "feat: xyz" --tool claude --conf high
ai-prov report file.py         # Generate report
ai-prov query --ai-percent     # Query metrics
ai-prov validate --require-review
ai-prov trace-matrix           # Traceability
```

## Environment Variables

None currently. All configuration is in git config or .gitattributes.

## Dependencies

### Runtime
- `click>=8.0.0` - CLI framework
- `gitpython>=3.1.0` - Git operations
- `pydantic>=2.0.0` - Data validation
- `rich>=13.0.0` - Terminal formatting
- `jinja2>=3.0.0` - Template rendering (unused currently)

### Development
- `pytest>=7.0.0` - Testing
- `pytest-cov>=4.0.0` - Coverage
- `black>=23.0.0` - Formatting
- `ruff>=0.1.0` - Linting
- `mypy>=1.0.0` - Type checking

## Essential Project Overview

AI Provenance solves the problem of "how do I track which code was AI-generated?" in a Git-native, language-agnostic, zero-dependency way. It's designed for:

- **Individual developers**: Track your own AI usage
- **Teams**: Enforce review policies for AI code
- **Enterprises**: Audit and compliance for AI contributions
- **Researchers**: Analyze AI coding patterns

The tool is distributed via PyPI and integrates seamlessly with existing Git workflows.

## Critical Implementation Details

### Git Notes Namespace

All commit metadata is stored in `refs/notes/ai-provenance`. To push notes:

```bash
git push origin refs/notes/ai-provenance
```

### Inline Metadata Parsing

Uses regex patterns to detect AI comments across languages. See `parsers/stamper.py` for full list of comment styles.

### Commit Message Format

Follows Conventional Commits + AI extension. The `[AI:tool:conf]` tag is optional but triggers validation in commit-msg hook.

### Metadata Schema

All metadata uses Pydantic models for validation. See `core/models.py` for schemas.

### Temporal Queries

Historical metadata is reconstructed by reading git notes at specific revisions. Use `git show <rev>:file.meta.json` for file-level metadata.

### Documentation and Help
- **User guide HTML generation**: Generate HTML versions of user guides from markdown sources
- **Dark mode support**: Provide both light and dark mode versions of documentation
- **Browser viewing**: Open user guides in default browser with mode selection
- **Pre-generated files**: Commit generated HTML files to repository for browser refresh capability
- **Helper scripts**: Provide scripts in helper directory for regenerating documentation

## Future Enhancements

1. **Filter driver**: Implement ai-prov-filter for auto .meta.json generation
2. **Tree-sitter**: Better function/class detection
3. **Diff analysis**: Track AI % over time
4. **Web dashboard**: Visualize metrics
5. **IDE integration**: VS Code extension
6. **Advanced queries**: SQL-like query language for metadata
