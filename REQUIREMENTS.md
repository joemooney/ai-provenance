# AI Provenance - Requirements

## Functional Requirements

### FR1: Metadata Tracking

#### FR1.1: Inline Metadata
- **REQ**: Support inline metadata comments in all common programming languages
- **Acceptance**: Detect and parse # // /* -- comment styles
- **Format**: `ai:tool:conf | trace:ID | test:ID | reviewed:DATE:USER`

#### FR1.2: Commit Metadata
- **REQ**: Store metadata in commit messages and git notes
- **Acceptance**: Parse `[AI:tool:conf]` tag and metadata fields
- **Format**: Conventional commit + AI extension

#### FR1.3: File Metadata
- **REQ**: Generate `.meta.json` files with file-level metadata
- **Acceptance**: JSON schema validation, hierarchical block data
- **Status**: Planned (filter driver not implemented)

#### FR1.4: Historical Metadata
- **REQ**: Reconstruct metadata for any git revision
- **Acceptance**: `ai-prov report --rev <sha>` works
- **Implementation**: Read git notes and .meta.json at specific commits

### FR2: Git Integration

#### FR2.1: Repository Initialization
- **REQ**: `ai-prov init` sets up hooks, filters, git notes
- **Acceptance**: Non-destructive, idempotent, backs up existing hooks
- **Components**: commit-msg, post-commit, pre-push hooks

#### FR2.2: Git Notes
- **REQ**: Store immutable metadata in `refs/notes/ai-provenance`
- **Acceptance**: CRUD operations, namespace isolation
- **Push**: Pre-push hook pushes notes automatically

#### FR2.3: Git Hooks
- **REQ**: Validate commits, add notes, push notes
- **Acceptance**: Hooks execute without errors, provide clear messages
- **Validation**: commit-msg validates AI tag format

### FR3: CLI Commands

#### FR3.1: ai-prov init
- **REQ**: Initialize repository
- **Output**: Success message, hook installation status
- **Options**: `--verbose` for detailed output

#### FR3.2: ai-prov stamp
- **REQ**: Add inline metadata to files
- **Input**: file path, tool, confidence, trace, tests, reviewer
- **Output**: Modified file with metadata comment
- **Position**: Top (default) or bottom

#### FR3.3: ai-prov commit
- **REQ**: Create commit with provenance metadata
- **Input**: message, tool, confidence, trace, tests, reviewer
- **Output**: Commit SHA, git note added
- **Format**: Structured message with AI tag

#### FR3.4: ai-prov report
- **REQ**: Generate file/repo reports
- **Input**: file path, revision, format (text/json/md)
- **Output**: Comprehensive metadata report
- **Content**: File metadata, commit notes, inline metadata

#### FR3.5: ai-prov query
- **REQ**: Query repository for AI metrics
- **Queries**: `--ai-percent`, `--unreviewed`, `--trace <id>`, `--by-file`
- **Output**: Formatted results
- **Aggregation**: Repo-wide or per-file

#### FR3.6: ai-prov validate
- **REQ**: Validate repository metadata integrity
- **Checks**: `--require-review`, `--require-tests`
- **Output**: List of validation errors or success
- **Exit**: Non-zero on failure

#### FR3.7: ai-prov trace-matrix
- **REQ**: Generate traceability matrix
- **Format**: md (default), json, html
- **Output**: Feature → Code → Tests mapping
- **Columns**: Feature, AI%, Commits, Files, Tests, Status

### FR4: Reporting & Analytics

#### FR4.1: AI Percentage Calculation
- **REQ**: Calculate % of AI-generated code
- **Scope**: File-level or repo-wide
- **Algorithm**: Count AI lines / total lines * 100
- **Breakdown**: By file, by tool, by confidence

#### FR4.2: Unreviewed Code Detection
- **REQ**: Find AI code without human review
- **Output**: List of commits/files needing review
- **Filter**: By date, by tool

#### FR4.3: Trace Mapping
- **REQ**: Link requirements to code and tests
- **Input**: Requirement ID (SPEC-xxx)
- **Output**: All commits, files, tests for that requirement
- **Matrix**: Bidirectional trace (req ↔ code ↔ test)

#### FR4.4: Temporal Analysis
- **REQ**: Analyze AI % over time
- **Status**: Planned
- **Output**: Time series data, graphs

### FR5: CI/CD Integration

#### FR5.1: GitHub Actions Template
- **REQ**: Ready-to-use workflow file
- **Features**: Validate, report, comment on PRs
- **Triggers**: Pull requests, pushes to main
- **Artifacts**: Metrics, traceability matrix

#### FR5.2: GitLab CI Template
- **REQ**: Pipeline configuration
- **Features**: Validate, report, MR comments
- **Artifacts**: Dotenv, metrics, reports

#### FR5.3: Validation Gates
- **REQ**: Block merges if validation fails
- **Checks**: Unreviewed AI code, missing tests
- **Override**: Manual approval possible

## Non-Functional Requirements

### NFR1: Performance

#### NFR1.1: Scalability
- **REQ**: Handle repos with 100K+ lines of code
- **Baseline**: < 5 seconds for full repo query
- **Large repos**: < 30 seconds

#### NFR1.2: Memory Efficiency
- **REQ**: Use < 500MB RAM for typical operations
- **Streaming**: Process large files line-by-line

#### NFR1.3: Git Operations
- **REQ**: Use GitPython efficiently
- **Caching**: Cache repo objects where possible

### NFR2: Compatibility

#### NFR2.1: Python Versions
- **REQ**: Support Python 3.8+
- **Testing**: CI tests on 3.8, 3.9, 3.10, 3.11, 3.12

#### NFR2.2: Operating Systems
- **REQ**: Works on Linux, macOS, Windows
- **Path handling**: Use `pathlib` for cross-platform paths

#### NFR2.3: Git Versions
- **REQ**: Works with Git 2.20+
- **Features**: Git notes, filters (2.20+)

### NFR3: Reliability

#### NFR3.1: Error Handling
- **REQ**: Graceful error messages for common failures
- **Examples**: File not found, invalid git repo, malformed metadata
- **Exit codes**: Standard POSIX codes

#### NFR3.2: Data Integrity
- **REQ**: Never corrupt git repository
- **Validation**: Pydantic models validate all metadata
- **Backups**: Backup existing hooks before overwriting

#### NFR3.3: Idempotency
- **REQ**: Commands can be run multiple times safely
- **Example**: `ai-prov init` doesn't fail if already initialized

### NFR4: Usability

#### NFR4.1: CLI UX
- **REQ**: Clear, helpful error messages
- **Help text**: Comprehensive `--help` for all commands
- **Progress**: Show progress for long operations

#### NFR4.2: Documentation
- **REQ**: README, examples, API docs
- **Coverage**: 100% of CLI commands documented
- **Examples**: Real-world use cases

#### NFR4.3: Onboarding
- **REQ**: < 5 minutes from install to first report
- **Tutorial**: Quick start guide in README

### NFR5: Maintainability

#### NFR5.1: Code Quality
- **REQ**: 100% type hints, docstrings
- **Tools**: Black, Ruff, Mypy
- **Standards**: PEP 8 compliance

#### NFR5.2: Test Coverage
- **REQ**: > 80% code coverage
- **Framework**: Pytest
- **CI**: Run tests on every commit

#### NFR5.3: Modularity
- **REQ**: Clear separation of concerns
- **Architecture**: CLI, core, git_integration, parsers, reporters
- **Coupling**: Low coupling, high cohesion

### NFR6: Security

#### NFR6.1: Input Validation
- **REQ**: Validate all user inputs
- **Pydantic**: Use models for validation
- **Injection**: Prevent command injection in git operations

#### NFR6.2: Privacy
- **REQ**: No data sent to external services
- **Offline**: Fully functional offline
- **Telemetry**: None

#### NFR6.3: Permissions
- **REQ**: Respect file permissions
- **Hooks**: Installed with 755 permissions
- **Files**: Don't modify permissions unnecessarily

## Data Requirements

### DR1: Metadata Schema

#### DR1.1: AITool Enum
- **Values**: claude, copilot, chatgpt, gemini, cursor, other
- **Extensible**: Easy to add new tools

#### DR1.2: Confidence Enum
- **Values**: high, med, low
- **Semantics**: high=copy-paste, med=modified, low=assisted

#### DR1.3: BlockMetadata
- **Fields**: kind, name, lines, ai, confidence, trace, tests
- **Validation**: lines[0] <= lines[1], kind in (function, class, method, block)

#### DR1.4: FileMetadata
- **Fields**: file, generated_at, ai_tool, confidence, trace, tests, reviewed_by, reviewed_at, blocks
- **Methods**: ai_percentage()

#### DR1.5: CommitMetadata
- **Fields**: ai_tool, confidence, trace, tests, reviewed_by, reviewed_at, files
- **Storage**: Git notes JSON

## Integration Requirements

### IR1: Version Control

#### IR1.1: Git
- **REQ**: Full Git integration via GitPython
- **Operations**: commit, notes, log, show, diff
- **Notes**: Use refs/notes/ai-provenance namespace

### IR2: Build Systems

#### IR2.1: PyPI
- **REQ**: Publishable to PyPI
- **Format**: Wheel + sdist
- **Metadata**: pyproject.toml PEP 621 compliant

#### IR2.2: Packaging
- **REQ**: Use setuptools for building
- **Entry point**: ai-prov CLI command
- **Dependencies**: Minimal, pinned versions

### IR3: CI/CD Platforms

#### IR3.1: GitHub Actions
- **REQ**: Template workflow file
- **API**: Use actions/github-script for PR comments

#### IR3.2: GitLab CI
- **REQ**: Template pipeline file
- **API**: Use GitLab API for MR comments

#### IR3.3: Others (Future)
- **Planned**: Jenkins, CircleCI, Azure Pipelines

## Compliance Requirements

### CR1: Licensing

#### CR1.1: Open Source
- **License**: MIT
- **Compatibility**: Compatible with all major licenses

### CR2: Attribution

#### CR2.1: AI Attribution
- **REQ**: Track which AI tool generated code
- **Purpose**: Compliance, analytics, debugging

#### CR2.2: Review Tracking
- **REQ**: Record human review of AI code
- **Field**: reviewed_by, reviewed_at

### CR3: Audit Trail

#### CR3.1: Immutability
- **REQ**: Git notes provide tamper-evident records
- **Verification**: Git cryptographic hashing

#### CR3.2: Traceability
- **REQ**: Full requirement → code → test trace
- **Matrix**: Generate traceability reports

## Future Requirements (Roadmap)

### Future: Filter Driver
- **REQ**: Auto-generate .meta.json on `git add`
- **Status**: Stubbed, not implemented

### Future: Tree-sitter Integration
- **REQ**: Better function/class detection
- **Benefit**: More accurate block metadata

### Future: Diff Analysis
- **REQ**: Track AI % changes over time
- **Output**: Time series data, graphs

### Future: Web Dashboard
- **REQ**: Visualize metrics in web UI
- **Tech**: Flask/FastAPI + Charts.js

### Future: IDE Integration
- **REQ**: VS Code extension
- **Features**: Highlight AI code, inline metrics

### Future: Advanced Queries
- **REQ**: SQL-like query language
- **Example**: `SELECT * FROM commits WHERE ai_tool='claude' AND confidence='high'`

## Constraints

### Technical Constraints
- **Git required**: Must have Git 2.20+
- **Python required**: Must have Python 3.8+
- **Text files only**: Binary files not supported

### Design Constraints
- **Git-native**: All data in Git
- **Language-agnostic**: No language-specific parsing (except future tree-sitter)
- **Zero external deps**: No cloud services

### Resource Constraints
- **Development**: Single developer initially
- **Budget**: Open source, no funding
- **Time**: MVP in 1 session
