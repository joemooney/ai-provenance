# AI Provenance Complete Walkthrough

This guide walks through creating a new project from scratch with AI provenance tracking and requirements-manager integration.

## Prerequisites

1. **Install requirements-manager**:
   ```bash
   cd /home/joe/ai/req/requirements-manager
   cargo build --release
   ```

2. **Install ai-provenance**:
   ```bash
   cd /home/joe/ai/ai-provenance
   pip install -e ".[dev]"
   ```

## Step-by-Step Walkthrough

### Step 1: Create Project Directory

```bash
mkdir ~/ai/demo-calculator
cd ~/ai/demo-calculator
```

### Step 2: Initialize Git Repository

```bash
git init
```

### Step 3: Initialize AI Provenance

```bash
ai-prov init
```

This creates:
- `.git/hooks/` - Git hooks for automatic metadata capture
- Git notes namespace `refs/notes/ai-provenance`
- Git config for AI provenance

### Step 4: Apply Feature Profile

```bash
ai-prov features profile standard
```

This enables:
- Inline metadata stamping
- Commit message validation
- Git notes tracking
- Query and reporting
- Traceability matrix

### Step 5: Scaffold Project Structure

```bash
ai-prov wizard scaffold
```

This creates:
- `.ai-prov/` - AI provenance data directory
- `.claude/commands/` - Claude Code slash commands:
  - `/ap-req` - Create requirements
  - `/ap-implement` - Implement features
  - `/ap-trace` - Check traceability
  - `/ap-stamp` - Add inline metadata
  - `/ap-doc` - Generate documentation
  - `/ap-release` - Check release readiness
- `.standards/` - Coding standards and conventions
- `docs/`, `specs/`, `tests/` - Standard directories

### Step 6: Initialize Requirements

Create empty requirements.yaml:
```bash
echo "requirements: []" > requirements.yaml
```

### Step 7: Create First Requirement

Use requirements-manager to create a requirement:

```bash
/home/joe/ai/req/requirements-manager/target/release/requirements-manager add \
  --title "Basic Calculator Operations" \
  --description "Implement add, subtract, multiply, and divide operations" \
  --feature Core \
  --priority High \
  --status Draft
```

Output:
```
Requirement added successfully!
ID: 67befb88-1a5a-4751-9032-8c5f349d45fb
```

### Step 8: Generate SPEC-ID Mapping

```bash
/home/joe/ai/req/requirements-manager/target/release/requirements-manager export --format mapping
```

This creates `.requirements-mapping.yaml`:
```yaml
mappings:
  67befb88-1a5a-4751-9032-8c5f349d45fb: SPEC-001
next_spec_number: 2
```

Now you can reference the requirement as **SPEC-001** in your code.

### Step 9: Implement the Requirement

Create `src/calculator.py`:

```python
"""
Simple calculator module.
"""


def add(a: float, b: float) -> float:
    # ai:claude:high | trace:SPEC-001
    """Add two numbers."""
    return a + b
    # /ai


def subtract(a: float, b: float) -> float:
    # ai:claude:high | trace:SPEC-001
    """Subtract b from a."""
    return a - b
    # /ai


def multiply(a: float, b: float) -> float:
    # ai:claude:high | trace:SPEC-001
    """Multiply two numbers."""
    return a * b
    # /ai


def divide(a: float, b: float) -> float:
    # ai:claude:high | trace:SPEC-001
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
    # /ai
```

Create `tests/test_calculator.py`:

```python
"""
Tests for calculator module.
"""
# ai:claude:high | trace:SPEC-001 | test:TC-001

import pytest
from src.calculator import add, subtract, multiply, divide


def test_add():
    """Test addition."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_subtract():
    """Test subtraction."""
    assert subtract(5, 3) == 2
    assert subtract(1, 1) == 0
    assert subtract(0, 5) == -5


def test_multiply():
    """Test multiplication."""
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6
    assert multiply(0, 5) == 0


def test_divide():
    """Test division."""
    assert divide(6, 3) == 2
    assert divide(5, 2) == 2.5

    with pytest.raises(ValueError):
        divide(5, 0)

# /ai
```

### Step 10: Commit with AI Provenance

```bash
git add -A
git commit -m "[AI:claude:high] feat(calculator): implement basic operations

Implement add, subtract, multiply, and divide operations with full test coverage.

Trace: SPEC-001
Test: TC-001

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

Output:
```
🤖 AI commit detected, validating metadata...
✅ AI commit validation passed
📝 Adding AI provenance metadata to git notes...
✅ AI provenance metadata added to commit 101dfd8d
```

### Step 11: Verify Traceability

#### Generate Traceability Matrix

```bash
ai-prov trace-matrix
```

Output:
```
# Traceability Matrix

| SPEC-ID | Title | Status | AI % | Commits | Files | Tests |
|---------|-------|--------|------|---------|-------|-------|
| SPEC-001 | Basic Calculator Operations | Draft | 100% | 1 | 0 | 1 |
```

#### Check AI Code Percentage

```bash
ai-prov query --ai-percent
```

Output:
```
AI-Generated Code: 18.00%
  Total lines: 800
  AI lines: 144
```

#### Generate File Report

```bash
ai-prov report src/calculator.py
```

Output:
```
AI Metadata Report: src/calculator.py @ HEAD

Commit Metadata:
  {
    "ai_tool": "claude",
    "confidence": "high",
    "trace": ["SPEC-001"],
    "tests": ["TC-001"]
  }

Inline Metadata:
  Line 7: {'tool': 'claude', 'confidence': 'high', 'trace': 'SPEC-001'}
  Line 14: {'tool': 'claude', 'confidence': 'high', 'trace': 'SPEC-001'}
  Line 21: {'tool': 'claude', 'confidence': 'high', 'trace': 'SPEC-001'}
  Line 28: {'tool': 'claude', 'confidence': 'high', 'trace': 'SPEC-001'}
```

#### View Git Notes

```bash
git notes --ref ai-provenance show
```

Output:
```json
{"ai_tool":"claude","confidence":"high","trace":["SPEC-001"],"tests":["TC-001"]}
```

## Summary

You've successfully created a project with:

✅ **Git initialization** with AI provenance hooks
✅ **Requirements management** via requirements-manager
✅ **SPEC-ID mapping** for traceability
✅ **Inline AI metadata** in code
✅ **Git commit metadata** with Trace: and Test: links
✅ **Git notes** for immutable provenance
✅ **Traceability matrix** showing complete links
✅ **AI percentage tracking** across the codebase

## Using Claude Code Slash Commands

If you're using Claude Code, you can use the slash commands created during scaffolding:

### `/ap-req` - Create Requirement
Interactive requirement creation using requirements-manager.

### `/ap-implement` - Implement Feature
Guided implementation of a requirement with automatic AI tagging.

### `/ap-trace` - Check Traceability
Verify traceability between requirements, code, and tests.

### `/ap-stamp` - Add Inline Metadata
Add AI metadata tags to existing code.

### `/ap-doc` - Generate Documentation
Generate HTML documentation from Markdown sources.

### `/ap-release` - Check Release Readiness
Analyze repository changes and determine if it's time for a new release. Checks:
- Recent activity (commits in last 7 days)
- Lines changed since last tag (threshold: 3000)
- Days since last release (threshold: 7)
- Suggests version number based on commit messages
- Provides release recommendation with detailed report

## Next Steps

1. **Add more requirements**:
   ```bash
   requirements-manager add -i
   requirements-manager export --format mapping
   ```

2. **Implement features with AI assistance** (in Claude Code):
   ```
   /ap-implement SPEC-002
   ```

3. **Review AI-generated code**:
   ```bash
   ai-prov query --unreviewed
   ai-prov validate --require-review
   ```

4. **Generate reports**:
   ```bash
   ai-prov trace-matrix
   ai-prov query --ai-percent --path src/
   ```

5. **Push git notes**:
   ```bash
   git push origin refs/notes/ai-provenance
   ```

## Architecture

```
demo-calculator/
├── requirements.yaml                  # requirements-manager (source of truth)
├── .requirements-mapping.yaml         # UUID → SPEC-ID mapping
├── .git/
│   ├── hooks/                        # AI provenance hooks
│   └── refs/notes/ai-provenance      # Commit metadata
├── .claude/commands/                 # Claude Code slash commands
├── src/calculator.py                 # Implementation (with inline tags)
└── tests/test_calculator.py          # Tests (with inline tags)
```

## Key Points

1. **Single Source of Truth**: requirements.yaml is managed by requirements-manager
2. **Direct Reading**: ai-provenance reads requirements.yaml directly (no export/import)
3. **Automatic Linking**: Trace: SPEC-XXX in commits creates traceability links
4. **Inline Metadata**: `# ai:tool:conf | trace:SPEC-XXX` tags code blocks
5. **Git Notes**: Immutable provenance metadata stored in Git
6. **Validation**: Pre-commit hooks validate metadata format
7. **Reporting**: Full traceability matrix and AI metrics

## Troubleshooting

### requirements-manager not found
Add to PATH or use full path:
```bash
export PATH="/home/joe/ai/req/requirements-manager/target/release:$PATH"
```

Or use full path in commands:
```bash
/home/joe/ai/req/requirements-manager/target/release/requirements-manager
```

### Git hooks not running
Ensure hooks are executable:
```bash
chmod +x .git/hooks/commit-msg
chmod +x .git/hooks/post-commit
chmod +x .git/hooks/pre-push
```

### Missing requirements.yaml
Create it first:
```bash
echo "requirements: []" > requirements.yaml
```

### AI percentage seems low
Make sure to:
1. Use inline metadata tags (`# ai:tool:conf`)
2. Include closing tags (`# /ai`)
3. Tag all AI-generated files (including support files)
