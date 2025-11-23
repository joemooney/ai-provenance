# Integration with requirements-manager (Simplified)

## Overview

AI Provenance integrates with [requirements-manager](https://github.com/joemooney/req) as its **sole requirements system**. This is a simplified architecture where:

- ✅ requirements-manager = ONLY place to manage requirements
- ✅ ai-provenance = Git metadata and traceability tracking
- ✅ No duplicate requirements storage
- ✅ Direct YAML reading (no export needed)

## Why This Approach?

Since ai-provenance is a new project with no existing requirements to migrate, we can simplify by **removing ai-provenance's native requirements system** entirely and depending on requirements-manager.

### What ai-provenance Does

- ✅ Read requirements from `requirements.yaml` directly
- ✅ Link commits to requirements via SPEC-IDs
- ✅ Generate traceability matrices
- ✅ Track AI attribution per requirement
- ✅ Calculate AI % by requirement
- ✅ Validate test coverage

### What ai-provenance Does NOT Do

- ❌ Store requirements in its own database
- ❌ Provide requirement CRUD commands
- ❌ Maintain `.ai-prov/requirements/` directory
- ❌ Duplicate requirements data

## Quick Start

### 1. Install requirements-manager

```bash
git clone https://github.com/joemooney/req
cd req/requirements-manager
cargo install --path .
```

### 2. Register Your Project

```bash
cd /home/joe/ai/ai-provenance

requirements-manager db register \
  --name ai-provenance \
  --path $(pwd)/requirements.yaml

requirements-manager db default ai-provenance
```

### 3. Create Requirements

```bash
# Create requirements using requirements-manager
requirements-manager add \
  --title "Git Integration" \
  --description "Support git hooks, notes, and filters" \
  --feature Core \
  --priority High \
  --status InProgress
```

### 4. Generate SPEC-ID Mapping

```bash
# Generate mapping file (UUID → SPEC-ID)
requirements-manager export --format mapping

# This creates .requirements-mapping.yaml:
# mappings:
#   f7d250bf-...: SPEC-001
#   013cc55c-...: SPEC-002
```

### 5. Link Code to Requirements

```bash
# Stamp file with AI metadata
ai-prov stamp src/auth.py \
  --tool claude \
  --conf high \
  --trace SPEC-001

# Commit with traceability
ai-prov commit \
  -m "feat: implement authentication" \
  --tool claude \
  --trace SPEC-001 \
  --test TC-101
```

### 6. Generate Reports

```bash
# ai-provenance reads requirements.yaml directly
ai-prov trace-matrix

# Output:
# | SPEC-ID | Title           | Commits | Files       | Tests  | AI % |
# |---------|-----------------|---------|-------------|--------|------|
# | SPEC-001| Authentication  | 3       | src/auth.py | TC-101 | 85%  |
```

## Architecture

```
┌─────────────────────────┐
│  requirements-manager   │  ← Source of Truth
│  (Rust CLI)             │
│  requirements.yaml      │  - Create/Edit/Delete requirements
└───────────┬─────────────┘  - Feature organization
            │                - Multi-project support
            │ Direct read
            ▼
┌─────────────────────────┐
│  ai-provenance          │  ← Traceability Layer
│  (Python CLI)           │
│  Git notes              │  - Read requirements.yaml
└─────────────────────────┘  - Link commits to SPEC-IDs
                              - Generate reports
```

## File Structure

```
project-root/
├── requirements.yaml              # Source of truth
├── .requirements-mapping.yaml     # UUID → SPEC-ID mapping
└── .git/
    └── refs/notes/ai-provenance  # Git notes with SPEC-ID references
```

**Note**: No `.ai-prov/requirements/` directory!

## Workflows

### Workflow 1: Feature Development

```bash
# 1. Create requirement (requirements-manager)
requirements-manager add -i
# → Feature: Authentication
# → Title: JWT token system
# → Output: Created SPEC-001

# 2. Implement with AI assistance
# (use Claude, Copilot, etc.)

# 3. Stamp code (ai-provenance)
ai-prov stamp src/jwt.py --tool claude --conf high --trace SPEC-001

# 4. Commit (ai-provenance)
ai-prov commit -m "feat: JWT tokens" --trace SPEC-001 --tool claude

# 5. Update status (requirements-manager)
requirements-manager edit <uuid> --status Completed

# 6. Generate matrix (ai-provenance)
ai-prov trace-matrix
```

### Workflow 2: Query Requirements

```bash
# List requirements
requirements-manager list [--feature FEATURE]

# Show details
requirements-manager show <UUID>

# Filter by status
requirements-manager list --status InProgress
```

### Workflow 3: Traceability Reporting

```bash
# Generate matrix
ai-prov trace-matrix [--format md|json|html]

# Find code for requirement
ai-prov query --trace SPEC-001

# Calculate AI %
ai-prov query --ai-percent

# Find unreviewed code
ai-prov query --unreviewed

# Validate coverage
ai-prov validate --require-tests
```

## Commands

### requirements-manager (Requirements Management)

```bash
# Create
requirements-manager add -i
requirements-manager add --title "..." --description "..." --feature FEATURE

# Read
requirements-manager list [--feature FEATURE] [--status STATUS]
requirements-manager show <UUID>

# Update
requirements-manager edit <UUID> --status Completed --priority High

# Export mapping
requirements-manager export --format mapping

# Multi-project
requirements-manager db register --name NAME --path PATH
requirements-manager db list
requirements-manager db default NAME
```

### ai-provenance (Git Metadata & Traceability)

```bash
# Initialize
ai-prov init

# Stamp and commit
ai-prov stamp FILE --tool TOOL --conf CONF --trace SPEC-ID
ai-prov commit -m MSG --tool TOOL --trace SPEC-ID --test TEST-ID

# Reports
ai-prov trace-matrix [--format md|json|html]
ai-prov report FILE

# Queries
ai-prov query --ai-percent [--by-file]
ai-prov query --unreviewed
ai-prov query --trace SPEC-ID

# Validation
ai-prov validate --require-tests --require-review
```

## Configuration

### Environment Variables

- `REQ_DB_NAME`: Project name (e.g., `ai-provenance`)
- `REQ_REGISTRY_PATH`: Registry location (default: `~/.requirements.config`)

### Example

```bash
export REQ_DB_NAME=ai-provenance
requirements-manager list
ai-prov trace-matrix
```

## Implementation Notes

### How ai-provenance Reads Requirements

Simple YAML parsing (no complex models):

```python
# src/ai_provenance/requirements.py (new, ~50 lines)

import yaml

def load_requirements(yaml_path="requirements.yaml"):
    """Load requirements from requirements-manager YAML."""
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    return data.get("requirements", [])

def load_mapping(mapping_path=".requirements-mapping.yaml"):
    """Load UUID → SPEC-ID mapping."""
    with open(mapping_path) as f:
        data = yaml.safe_load(f)
    return data.get("mappings", {})
```

### What Was Removed

- `src/ai_provenance/requirements/manager.py` (requirement CRUD)
- `src/ai_provenance/requirements/models.py` (Requirement, TestCase models)
- Requirement CLI commands
- `.ai-prov/requirements/` directory

### What Was Added

- Simple `requirements.py` module (~50 lines)
- Direct YAML reading in `traceability.py`

## Migration from Native Requirements

If you have existing ai-provenance requirements in `.ai-prov/requirements/*.json`:

```bash
# 1. Create requirements.yaml from JSON files
for json_file in .ai-prov/requirements/*.json; do
  # Extract fields and create requirement
  requirements-manager add \
    --title "$(jq -r .title $json_file)" \
    --description "$(jq -r .description $json_file)" \
    # ... other fields
done

# 2. Generate mapping
requirements-manager export --format mapping

# 3. Remove old JSON files
rm -rf .ai-prov/requirements/

# 4. Update code to use new system
# (ai-provenance will automatically read requirements.yaml)
```

## Benefits

### Compared to Native Requirements

| Aspect | Native (Old) | requirements-manager (New) |
|--------|--------------|----------------------------|
| Requirements storage | `.ai-prov/requirements/*.json` | `requirements.yaml` |
| CRUD commands | Built into ai-provenance | Dedicated tool |
| Code complexity | 500+ lines | ~50 lines |
| Multi-project support | No | Yes (via registry) |
| Type safety | Pydantic models | Rust types |
| Performance | Python | Rust |
| Feature organization | Manual | Auto-numbered |

### For Users

1. **Single tool** for requirements management
2. **Multi-project** support out of the box
3. **Faster** operations (Rust vs Python)
4. **Simpler** - no duplicate storage
5. **Cleaner** - one file to manage

### For Developers

1. **Less code** to maintain
2. **Clear separation** of concerns
3. **No sync issues**
4. **Easier testing**
5. **Better architecture**

## Troubleshooting

### "No requirements found"

Ensure `requirements.yaml` exists:

```bash
requirements-manager list
```

If empty, create requirements:

```bash
requirements-manager add -i
```

### "SPEC-ID not found in mapping"

Regenerate mapping file:

```bash
requirements-manager export --format mapping
```

### "Cannot find requirements-manager"

Install and add to PATH:

```bash
cd /path/to/requirements-manager
cargo install --path .
```

## See Also

- [requirements-manager](https://github.com/joemooney/req) - Requirements management tool
- [INTEGRATION_v2.md](https://github.com/joemooney/req/blob/main/INTEGRATION_v2.md) - Complete integration guide
- [SIMPLIFIED_INTEGRATION.md](https://github.com/joemooney/req/blob/main/SIMPLIFIED_INTEGRATION.md) - Implementation details

## Support

- requirements-manager issues: https://github.com/joemooney/req/issues
- ai-provenance issues: https://github.com/joemooney/ai-provenance/issues

---

**Note**: This replaces the previous `INTEGRATION.md` which described a more complex export/import system. The simplified approach is recommended for all new projects.
