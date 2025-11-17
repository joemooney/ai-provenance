# Requirements Management Workflow

## Overview

AI Provenance uses a **two-tier requirements architecture** that balances human readability with machine automation:

1. **Human-Readable Specs** (`specs/requirements/*.md`) - IEEE-830 inspired Markdown with YAML front-matter
2. **Machine-Processable Data** (`.ai-prov/requirements/*.json`) - Pure JSON for CLI and automation

## Architecture

```
Project Root
├── specs/requirements/           # Source of Truth (Human-First)
│   ├── SPEC-0001.md             # Markdown + YAML front-matter
│   ├── SPEC-0002.md             # Full IEEE-830 template
│   └── TEMPLATE.md              # Template for new requirements
│
├── .ai-prov/requirements/        # Derived Data (Machine-First)
│   ├── SPEC-0001.json           # Auto-generated from Markdown
│   ├── SPEC-0002.json           # Used by CLI, queries, reports
│   └── ...
│
└── .ai-prov/tests/               # Test Cases
    ├── TC-001.json
    └── ...
```

## Markdown Template (IEEE-830 Style)

Located at: `src/ai_provenance/requirements/templates/ieee830.md`

### Structure

```markdown
---
id: SPEC-0123
version: 1.0
status: Draft
priority: High
ai_generated: true
ai_tool: claude
ai_confidence: high
authors:
  - alice@example.com
reviewers:
  - bob@example.com
reviewed_at: 2025-11-16T14:30:00Z
parent: EPIC-45
tags: [auth, security, oauth]
---

# SPEC-0123: JWT Token Refresh Endpoint

## 1. Requirement Statement
The system **shall** provide...

## 2. Rationale
Why this requirement exists...

## 3. Source
- Stakeholder: Product Owner
- Reference: [PRD v3.1]

## 4. Fit Criterion (Verification)
| Test Case | Expected Result |
|-----------|-----------------|
| TC-210    | POST /auth/refresh → 200 OK |

## 5. Dependencies
- SPEC-0089
- SPEC-0090

## 6. Assumptions
- Clock skew ≤ 30 seconds

## 7. Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Token replay | Low | High | One-time use |

## 8. Open Issues
- [ ] Support PKCE?

## 9. Change History
| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2025-11-16 | alice | Initial |
```

### Benefits

✅ **Human-readable** - Markdown with clear structure
✅ **Machine-parsable** - YAML front-matter for automation
✅ **Git-friendly** - Text-based, excellent diffs
✅ **Compliance-ready** - IEEE-830, DO-178C, ASPICE compatible
✅ **Traceable** - Built-in links to parent, tests, dependencies
✅ **AI-aware** - ai_generated, ai_tool, reviewers fields

## JSON Format

Located at: `.ai-prov/requirements/SPEC-XXX.json`

### Structure

```json
{
  "id": "SPEC-0123",
  "title": "JWT Token Refresh Endpoint",
  "description": "The system shall provide...",
  "type": "feature",
  "status": "implemented",
  "priority": "high",
  "created_at": "2025-11-16T14:00:00Z",
  "updated_at": "2025-11-16T15:30:00Z",
  "created_by": "alice@example.com",
  "parent": "EPIC-45",
  "children": [],
  "related": ["SPEC-0089", "SPEC-0090"],
  "files": ["src/auth/refresh.py"],
  "commits": ["abc123"],
  "tests": ["TC-210", "TC-211"],
  "ai_generated": true,
  "ai_tool": "claude",
  "tags": ["auth", "security"],
  "acceptance_criteria": [
    "Valid refresh token → new access token",
    "Invalid token → 401"
  ]
}
```

### Benefits

✅ **Fast queries** - Programmatic access via RequirementManager
✅ **Pydantic validation** - Type-safe with auto-validation
✅ **CLI integration** - Used by all ai-prov commands
✅ **Traceability** - Direct links to files, commits, tests

## Workflow

### 1. Create New Requirement

```bash
# Option A: Generate from template
ai-prov requirement create SPEC-0123 \
  --title "JWT Token Refresh" \
  --description "Implement refresh endpoint" \
  --template ieee830

# Creates:
# - specs/requirements/SPEC-0123.md (full template)
# - .ai-prov/requirements/SPEC-0123.json (extracted from YAML)
```

```bash
# Option B: Manual creation
# 1. Copy specs/requirements/TEMPLATE.md
# 2. Fill in sections
# 3. Sync to JSON
ai-prov requirement sync --md-to-json
```

### 2. Edit Requirement

**Edit the Markdown file** (source of truth):
```bash
vim specs/requirements/SPEC-0123.md
```

**Sync changes to JSON**:
```bash
ai-prov requirement sync --md-to-json
# or
git commit  # Pre-commit hook auto-syncs
```

### 3. Link to Code

```bash
# Add trace comment in code
# ai:claude:high | trace:SPEC-0123 | test:TC-210

# Link file to requirement
ai-prov requirement link SPEC-0123 --file src/auth/refresh.py

# Updates SPEC-0123.json with file reference
```

### 4. Create Test Cases

```bash
ai-prov test create TC-210 \
  --title "Test JWT refresh" \
  --requirement SPEC-0123 \
  --file tests/test_auth.py

# Updates:
# - .ai-prov/tests/TC-210.json
# - .ai-prov/requirements/SPEC-0123.json (adds TC-210 to tests array)
```

### 5. Generate Traceability Matrix

```bash
ai-prov trace-matrix --format markdown

# Output:
# | SPEC      | Status      | AI    | Tests      | Files           |
# |-----------|-------------|-------|------------|-----------------|
# | SPEC-0123 | Implemented | ✓ High| TC-210,211 | src/auth/refresh.py |
```

## Synchronization

### Markdown → JSON (Primary Flow)

```bash
ai-prov requirement sync --md-to-json
```

- Reads all `specs/requirements/SPEC-*.md`
- Parses YAML front-matter
- Extracts structured sections (fit criteria, dependencies)
- Generates/updates `.ai-prov/requirements/SPEC-*.json`

### JSON → Markdown (Rare)

```bash
ai-prov requirement sync --json-to-md --template ieee830
```

- Reads all `.ai-prov/requirements/SPEC-*.json`
- Applies IEEE-830 template
- Generates `specs/requirements/SPEC-*.md`
- **Warning**: Overwrites existing Markdown!

### Auto-Sync (Recommended)

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Auto-sync requirements on commit
ai-prov requirement sync --md-to-json --quiet
git add .ai-prov/requirements/*.json
```

## Best Practices

### 1. **Markdown is Source of Truth**

- Edit requirements in `specs/requirements/*.md`
- JSON files are **derived** (auto-generated)
- Never manually edit JSON files

### 2. **Version Control**

```bash
# Commit both formats together
git add specs/requirements/SPEC-0123.md
git add .ai-prov/requirements/SPEC-0123.json
git commit -m "[AI:claude:high] feat: add JWT refresh requirement

Trace: SPEC-0123"
```

### 3. **Review Process**

1. Create requirement in Draft status
2. Add to `reviewers` list in YAML front-matter
3. Review → Update `status: Approved`
4. Update `reviewed_at` timestamp
5. Sync and commit

### 4. **AI Generation**

When AI generates a requirement:

```yaml
---
ai_generated: true
ai_tool: claude
ai_confidence: high
reviewers:
  - human@example.com  # Must add human reviewer
reviewed_at: null      # Pending review
status: Draft          # Start in draft
---
```

### 5. **Traceability**

Always link requirements to:
- **Parent** (epic, user story)
- **Tests** (in fit criterion table)
- **Dependencies** (other requirements)
- **Files** (via inline comments or CLI)

## Migration from Existing Systems

### From Jira/Linear

1. Export requirements to CSV
2. Convert to Markdown using script:

```bash
python scripts/import_from_csv.py jira_export.csv \
  --template ieee830 \
  --output specs/requirements/
```

3. Sync to JSON:

```bash
ai-prov requirement sync --md-to-json
```

### From Existing Markdown

If you have existing `*.md` requirements without YAML:

1. Add YAML front-matter manually
2. Or use conversion script:

```bash
python scripts/add_frontmatter.py specs/requirements/*.md
```

## CLI Commands Reference

```bash
# Create
ai-prov requirement create SPEC-XXX --title "..." --description "..." [--template ieee830]

# List
ai-prov requirement list [--status approved] [--type feature]

# Show
ai-prov requirement show SPEC-XXX [--format md|json]

# Link
ai-prov requirement link SPEC-XXX --file path/to/file.py
ai-prov requirement link SPEC-XXX --commit abc123
ai-prov requirement link SPEC-XXX --test TC-210

# Sync
ai-prov requirement sync [--md-to-json | --json-to-md] [--template ieee830]

# Query
ai-prov requirement find --untested
ai-prov requirement find --by-file src/auth.py
ai-prov requirement find --by-status draft

# Traceability
ai-prov trace-matrix [--format md|json|html]
```

## Example: Complete Requirement Lifecycle

```bash
# 1. Create requirement
ai-prov requirement create SPEC-0200 \
  --title "Rate limiting for API" \
  --description "Implement token bucket rate limiter" \
  --priority high \
  --template ieee830

# 2. Edit Markdown (add details, fit criteria, risks)
vim specs/requirements/SPEC-0200.md

# 3. Create test case
ai-prov test create TC-400 \
  --title "Test rate limiter" \
  --requirement SPEC-0200 \
  --file tests/test_rate_limit.py

# 4. Implement feature (with inline metadata)
cat > src/rate_limiter.py <<EOF
# ai:claude:high | trace:SPEC-0200 | test:TC-400

class TokenBucketLimiter:
    # Implementation...
EOF

# 5. Link file to requirement
ai-prov requirement link SPEC-0200 --file src/rate_limiter.py

# 6. Commit with provenance
ai-prov commit -m "feat: implement rate limiter" \
  --tool claude --conf high \
  --trace SPEC-0200 --test TC-400

# 7. Mark as implemented
vim specs/requirements/SPEC-0200.md  # Update status: Implemented

# 8. Sync and verify
ai-prov requirement sync --md-to-json
ai-prov requirement show SPEC-0200
ai-prov trace-matrix | grep SPEC-0200

# 9. Final commit
git add .
git commit -m "[AI:claude:high] docs: complete SPEC-0200 implementation

Trace: SPEC-0200
Test: TC-400"
```

## Compliance & Auditing

The two-tier system supports:

- **DO-178C** (aviation software)
- **ISO 26262** (automotive)
- **IEC 62304** (medical devices)
- **ASPICE** (automotive SPICE)
- **IEEE-830** (software requirements)

All traceability links are bidirectional and stored in Git for full audit trail.

## Future Enhancements

- [ ] Web dashboard for requirements browsing
- [ ] Import/export to Jira, Linear, GitHub Issues
- [ ] Automated requirement validation in CI
- [ ] Requirements coverage reports
- [ ] AI-powered requirement generation from prompts
- [ ] Requirement dependency graph visualization
