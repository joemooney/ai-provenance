# AI Provenance Examples

This directory contains examples demonstrating AI provenance tracking.

## Files

### `sample_project.py`

A complete example showing:
- AI-generated functions with different confidence levels
- Inline metadata comments
- Manual (non-AI) code for comparison
- Proper tagging with trace IDs and test cases

### Running the Example

```bash
# 1. Initialize AI provenance in this directory
cd examples
git init
ai-prov init

# 2. Add the sample file
git add sample_project.py

# 3. Commit with provenance metadata
ai-prov commit -m "feat: add sample project" \
  --tool claude --conf high \
  --trace SPEC-001,SPEC-002,SPEC-003 \
  --test TC-001,TC-002,TC-003 \
  --reviewer alice@example.com

# 4. Generate report
ai-prov report sample_project.py

# 5. Query AI percentage
ai-prov query --ai-percent

# 6. Generate traceability matrix
ai-prov trace-matrix
```

## Metadata Levels

### High Confidence
```python
# ai:claude:high | trace:SPEC-001 | test:TC-001 | reviewed:2025-11-16:alice
def ai_generated_function():
    pass
```

Used when code is largely copy-pasted from AI with minimal modifications.

### Medium Confidence
```python
# ai:copilot:med | trace:SPEC-002 | test:TC-002 | reviewed:2025-11-16:bob
class PartiallyAIGenerated:
    pass
```

Used when AI provided the structure but human made significant changes.

### Low Confidence
```python
# ai:chatgpt:low | trace:SPEC-003 | reviewed:2025-11-16:charlie
def mostly_human_written():
    pass
```

Used when AI provided suggestions but the code is mostly human-written.

## Best Practices

1. **Always tag AI code**: Use inline comments for all AI-generated code
2. **Link to requirements**: Use `trace:SPEC-xxx` to link code to specifications
3. **Reference tests**: Use `test:TC-xxx` to link to test cases
4. **Require review**: Always include `reviewed:DATE:REVIEWER` after human review
5. **Use appropriate confidence**: Be honest about the level of AI contribution

## Workflow Example

```bash
# 1. Generate code with AI tool (e.g., Claude, Copilot)

# 2. Add inline metadata
ai-prov stamp my_file.py --tool claude --conf high \
  --trace SPEC-123 --test TC-456 --reviewer alice@example.com

# 3. Review the code manually

# 4. Commit with provenance
ai-prov commit -m "feat: add new feature" \
  --tool claude --conf high \
  --trace SPEC-123 --test TC-456

# 5. Generate reports
ai-prov report my_file.py
ai-prov query --ai-percent --by-file
ai-prov trace-matrix > TRACEABILITY.md
```

## CI/CD Integration

See `../src/ai_provenance/ci_templates/` for GitHub Actions and GitLab CI templates.

Example `.github/workflows/ai-provenance.yml`:

```yaml
name: AI Provenance

on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install ai-provenance
      - run: ai-prov validate --require-review --require-tests
      - run: ai-prov query --ai-percent >> $GITHUB_STEP_SUMMARY
```

## Queries

```bash
# What % of code is AI-generated?
ai-prov query --ai-percent --by-file

# Find unreviewed AI code
ai-prov query --unreviewed

# Find code for a specific requirement
ai-prov query --trace SPEC-123

# Validate repository
ai-prov validate --require-review --require-tests
```

## Reports

```bash
# File-level report
ai-prov report sample_project.py

# Historical report
ai-prov report sample_project.py --rev HEAD~3

# JSON format
ai-prov report sample_project.py --format json

# Markdown format
ai-prov report sample_project.py --format md
```

## Traceability Matrix

```bash
# Markdown format (default)
ai-prov trace-matrix

# JSON format
ai-prov trace-matrix --format json

# HTML format
ai-prov trace-matrix --format html > traceability.html

# Save to file
ai-prov trace-matrix --output TRACEABILITY.md
```

This generates a matrix showing:
- Feature/requirement IDs
- % AI-generated
- Commits implementing the feature
- Files affected
- Test cases covering the feature
- Review status
