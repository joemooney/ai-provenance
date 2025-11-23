# Integration with requirements-manager

## Overview

AI Provenance can integrate with [requirements-manager](https://github.com/yourusername/requirements-manager), a Rust-based CLI tool for managing requirements. This integration provides:

- **Centralized requirements database** across multiple projects
- **Rich CLI** for requirements CRUD operations
- **Multi-project registry** support
- **Automatic traceability** from requirements to code and tests
- **Bidirectional linking** between git commits and requirements

## Why Integrate?

**ai-provenance** excels at:
- Git integration and commit metadata
- AI code attribution and provenance tracking
- Traceability matrices
- Compliance and audit reporting

**requirements-manager** excels at:
- Structured requirements management
- Feature-based organization
- Multi-project support
- Fast, type-safe operations (Rust)

Together, they provide a complete solution for requirements tracking and AI code provenance.

## Quick Start

### 1. Install requirements-manager

```bash
# Install from source
git clone https://github.com/yourusername/requirements-manager
cd requirements-manager
cargo install --path .
```

### 2. Register Your Project

```bash
cd /home/joe/ai/ai-provenance
requirements-manager db register \
  --name ai-provenance \
  --path $(pwd)/requirements.yaml \
  --description "AI provenance tracking tool"

# Set as default
requirements-manager db default ai-provenance
```

### 3. Create Requirements

```bash
# Interactive mode
requirements-manager add -i

# Or CLI mode
requirements-manager add \
  --title "JWT Authentication" \
  --description "Implement JWT-based auth with refresh tokens" \
  --feature Authentication \
  --priority High \
  --status Draft
```

### 4. Link Requirements to Code

```bash
# Stamp file with AI metadata and requirement trace
ai-prov stamp src/auth.py \
  --tool claude \
  --conf high \
  --trace SPEC-001

# Commit with traceability
ai-prov commit \
  -m "feat(auth): implement JWT token generation" \
  --tool claude \
  --conf high \
  --trace SPEC-001 \
  --test TC-101
```

### 5. Generate Traceability Matrix

```bash
# ai-provenance reads from requirements.yaml
ai-prov trace-matrix --format md

# Output shows full traceability:
# Requirement → Files → Commits → Tests → AI %
```

## Configuration

Enable requirements-manager integration in `.ai-prov/config.yaml`:

```yaml
requirements:
  # Use requirements-manager as source
  source: requirements-manager

  # Path to requirements.yaml
  path: requirements.yaml

  # UUID to SPEC-ID mapping file
  mapping: .requirements-mapping.yaml
```

## Workflows

### Workflow: Feature Development

```bash
# 1. Create requirement
requirements-manager add -i
# → Feature: User-Management
# → Title: Password reset flow
# → Output: Created SPEC-042

# 2. Implement with AI assistance
# (use Claude, Copilot, etc.)

# 3. Stamp files
ai-prov stamp src/password_reset.py --tool claude --conf high --trace SPEC-042

# 4. Commit with metadata
ai-prov commit -m "feat: password reset" --trace SPEC-042 --test TC-500

# 5. Update requirement status
requirements-manager edit <uuid> --status Completed

# 6. Validate
ai-prov validate --require-review --require-tests
```

### Workflow: Query and Reporting

```bash
# List requirements by feature
requirements-manager list --feature Authentication

# Show requirement details
requirements-manager show <uuid>

# Generate traceability matrix
ai-prov trace-matrix

# Find unreviewed AI code
ai-prov query --unreviewed

# Calculate AI percentage
ai-prov query --ai-percent
```

## Data Model Mapping

| requirements-manager | ai-provenance | Notes |
|---------------------|---------------|-------|
| UUID | SPEC-{N} | Generated mapping maintained in `.requirements-mapping.yaml` |
| title | title | Direct mapping |
| description | description | Direct mapping |
| status | status | Enum mapping (Draft→planned, Completed→implemented) |
| priority | priority | Enum mapping (High→high, Medium→medium, Low→low) |
| feature | tags | Feature added as tag |
| dependencies | related | UUID converted to SPEC-ID |

## File Structure

```
project-root/
├── requirements.yaml                  # requirements-manager database
├── .requirements-mapping.yaml         # UUID ↔ SPEC-ID mapping
├── .ai-prov/
│   ├── config.yaml                   # ai-provenance configuration
│   ├── requirements/                 # Generated from requirements.yaml
│   │   ├── SPEC-001.json
│   │   ├── SPEC-002.json
│   │   └── ...
│   ├── tests/
│   │   └── TC-001.json
│   └── traces/
│       └── *.json
└── .git/
    └── refs/notes/ai-provenance
```

## Commands

### requirements-manager Commands

```bash
# CRUD operations
requirements-manager add [--title] [--description] [--feature] ...
requirements-manager list [--feature FEATURE] [--status STATUS]
requirements-manager show <UUID>
requirements-manager edit <UUID> [--title] [--status] ...

# Feature management
requirements-manager feature list
requirements-manager feature rename <old> <new>

# Database management
requirements-manager db register --name NAME --path PATH
requirements-manager db list
requirements-manager db default NAME

# Export (for ai-provenance)
requirements-manager export --format ai-prov --output .ai-prov/requirements/
```

### ai-provenance Commands (with integration)

```bash
# Traceability (reads requirements.yaml)
ai-prov trace-matrix [--format md|json|html]

# Validation
ai-prov validate --require-tests --require-review

# Queries
ai-prov query --ai-percent [--by-file]
ai-prov query --unreviewed
ai-prov query --trace SPEC-001

# Reports (includes requirement links)
ai-prov report src/auth.py
ai-prov report --format json
```

## Environment Variables

- `REQ_DB_NAME`: Project name in registry (e.g., `ai-provenance`)
- `REQ_REGISTRY_PATH`: Path to registry file (default: `~/.requirements.config`)
- `AI_PROV_REQ_SOURCE`: Requirements source (`requirements-manager` or `native`)

## Migration from Native Requirements

If you have existing requirements in `.ai-prov/requirements/*.json`:

```bash
# 1. Import to requirements-manager
requirements-manager import --from ai-prov --path .ai-prov/requirements/

# 2. Update config to use requirements-manager
echo "requirements:
  source: requirements-manager
  path: requirements.yaml
  mapping: .requirements-mapping.yaml" >> .ai-prov/config.yaml

# 3. Verify
requirements-manager list
ai-prov trace-matrix
```

## Benefits

1. **Multi-project support**: Manage requirements across all your projects from one tool
2. **Performance**: Rust-based requirements-manager is fast for large datasets
3. **Type safety**: Structured data with validation
4. **Feature organization**: Auto-numbered features with hierarchical organization
5. **Clean separation**: requirements-manager for CRUD, ai-provenance for git/traceability
6. **Shared registry**: One central registry at `~/.requirements.config`

## Troubleshooting

### Issue: "Requirement SPEC-001 not found"

**Solution**: Ensure mapping file exists and requirements.yaml is up to date:

```bash
# Regenerate mapping
requirements-manager export --format ai-prov
```

### Issue: "No requirements loaded"

**Solution**: Check config and paths:

```bash
# Verify config
cat .ai-prov/config.yaml

# Verify requirements file
requirements-manager list
```

### Issue: "UUID/SPEC-ID mismatch"

**Solution**: Regenerate mapping file:

```bash
rm .requirements-mapping.yaml
requirements-manager export --format ai-prov
```

## See Also

- [requirements-manager README](https://github.com/yourusername/requirements-manager)
- [Integration Architecture](../req/INTEGRATION.md) - Detailed technical design
- [AI Provenance Documentation](./README.md)

## Contributing

To improve the integration:

1. Report issues in respective repositories
2. Suggest features via GitHub Issues
3. Submit PRs for adapter improvements
4. Share use cases and workflows

## Support

- requirements-manager: https://github.com/yourusername/requirements-manager/issues
- ai-provenance: https://github.com/yourusername/ai-provenance/issues
