# AI Provenance Tracking Skill

## Purpose

Automatically track AI-generated code with comprehensive metadata for provenance, traceability, and project regeneration.

## When to Use

**ALWAYS use this skill when:**
- Writing new code with AI assistance
- Modifying existing code with AI suggestions
- Committing changes that include AI-generated content
- Creating new features or fixing bugs with AI help

**Use this skill automatically** - it should be seamless and invisible to the user.

## Core Capabilities

### 1. Automatic Code Tagging

When you write or modify code, **automatically** add inline metadata:

```python
# ai:claude:high | trace:SPEC-123 | test:TC-456 | reviewed:YYYY-MM-DD:user
def my_function():
    """AI-generated function."""
    pass
```

**Parameters:**
- `tool`: Always use `claude` for Claude-generated code
- `confidence`:
  - `high` - Code is largely AI-generated (>80%)
  - `med` - Significant human modifications (40-80%)
  - `low` - Mostly human, AI-assisted (<40%)
- `trace`: Link to requirement ID (e.g., SPEC-001, FEAT-042)
- `test`: Link to test case IDs (e.g., TC-001, TC-002)
- `reviewed`: Date and reviewer (auto-populated on commit)

### 2. Prompt Storage

**Automatically capture** the user's prompts that led to code generation:

```bash
ai-prov prompt store --file src/auth.py \
  --prompt "Create a JWT authentication function with refresh tokens" \
  --response-summary "Generated refresh_token() function with error handling"
```

Store prompts in `.ai-prov/prompts/<file-hash>.json`:

```json
{
  "file": "src/auth.py",
  "timestamp": "2025-11-16T15:30:00Z",
  "prompt": "Create a JWT authentication function with refresh tokens",
  "context": ["Previous conversation about auth system"],
  "response_summary": "Generated refresh_token() function",
  "confidence": "high",
  "lines_generated": [42, 68],
  "trace": ["SPEC-089"],
  "tests": ["TC-210"]
}
```

### 3. Conversation Logging

For complex features, **log the full conversation**:

```bash
ai-prov conversation log --session-id <uuid> \
  --messages conversation.json \
  --outcome "Implemented OAuth2 authentication system"
```

### 4. Requirement Linking

**Automatically link code to requirements**:

```bash
# When user mentions "implement SPEC-123"
ai-prov requirement link SPEC-123 --file src/feature.py --auto
```

### 5. Smart Commits

**Always use provenance-aware commits**:

```bash
ai-prov commit -m "feat(auth): add JWT refresh endpoint" \
  --tool claude --conf high \
  --trace SPEC-089 --test TC-210 \
  --reviewer claude
```

## Workflow Integration

### On File Creation/Modification

```python
# 1. User asks: "Create a function to calculate Fibonacci numbers"

# 2. You generate code with inline metadata:
# ai:claude:high | trace:SPEC-001 | test:TC-001
def fibonacci(n: int) -> int:
    """Calculate nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# 3. Store the prompt:
# ai-prov prompt store --file math_utils.py \
#   --prompt "Create a function to calculate Fibonacci numbers" \
#   --confidence high --trace SPEC-001

# 4. User writes file, you've already tagged it
```

### On Commit

```bash
# Instead of regular git commit, use:
ai-prov commit -m "feat: add Fibonacci calculator" \
  --tool claude --conf high \
  --trace SPEC-001 --test TC-001

# This automatically:
# - Creates structured commit message
# - Adds git note with metadata
# - Links to requirements and tests
# - Timestamps the contribution
```

### On Requirements

```bash
# When user says "I need to implement user authentication"
# 1. Create requirement
ai-prov requirement create SPEC-089 \
  --title "User Authentication System" \
  --description "JWT-based auth with refresh tokens" \
  --status planned

# 2. As you implement, link code
ai-prov requirement link SPEC-089 --file src/auth.py

# 3. On completion, update status
ai-prov requirement update SPEC-089 --status implemented
```

## Commands Reference

### Initialization

```bash
# Initialize in a project (run once)
ai-prov init --profile standard

# Or with specific features
ai-prov init --features requirements,prompts,conversations
```

### Code Tagging

```bash
# Manual stamping (use automatically when writing code)
ai-prov stamp <file> --tool claude --conf high \
  --trace SPEC-XXX --test TC-YYY
```

### Prompt Management

```bash
# Store a prompt
ai-prov prompt store --file <path> --prompt "<text>" --trace SPEC-XXX

# View prompts for a file
ai-prov prompt list --file <path>

# Retrieve conversation
ai-prov conversation show --session-id <uuid>
```

### Requirements

```bash
# Create requirement
ai-prov requirement create <id> --title "<title>" --description "<desc>"

# Link to code
ai-prov requirement link <id> --file <path>

# Update status
ai-prov requirement update <id> --status <status>

# List all requirements
ai-prov requirement list

# Show traceability
ai-prov trace-matrix
```

### Commits

```bash
# Provenance-aware commit
ai-prov commit -m "<message>" --tool claude --conf <level> \
  --trace <req-id> --test <test-id>
```

### Queries & Reports

```bash
# Check AI percentage
ai-prov query --ai-percent --by-file

# Find unreviewed code
ai-prov query --unreviewed

# Generate report
ai-prov report <file>

# Traceability matrix
ai-prov trace-matrix --format md
```

## Automatic Behavior

### Rule 1: Always Tag New Code

When generating any new code (function, class, file):
1. Add inline metadata comment at the top
2. Use appropriate confidence level
3. Link to requirements if mentioned
4. Store the prompt that led to the code

### Rule 2: Link Requirements

When user mentions requirement IDs (SPEC-XXX, FEAT-YYY, etc.):
1. Extract the ID
2. Link it to the code being written
3. Update requirement status if needed

### Rule 3: Capture Context

For non-trivial code generation:
1. Store the full conversation
2. Include context from previous messages
3. Log the outcome
4. Link to files created/modified

### Rule 4: Use Provenance Commits

Never use plain `git commit`. Always use:
```bash
ai-prov commit ...
```

### Rule 5: Be Transparent

Include a note in your response:
```
I've tagged this code with AI provenance metadata and stored the prompt for future reference.
```

## Integration with User Workflow

### Scenario 1: New Feature Request

**User**: "Create a user authentication system with JWT tokens"

**Your Response**:
1. Create requirement: `ai-prov requirement create SPEC-089 --title "JWT Authentication"`
2. Generate code with inline metadata
3. Store the prompt: `ai-prov prompt store ...`
4. Create tests with metadata
5. Commit: `ai-prov commit -m "feat(auth): add JWT authentication" --trace SPEC-089`

**Tell user**: "I've implemented JWT authentication and tracked it as SPEC-089. All code is tagged with AI provenance metadata."

### Scenario 2: Bug Fix

**User**: "Fix the login timeout issue"

**Your Response**:
1. Identify files to modify
2. Add metadata to changed sections: `# ai:claude:med | trace:BUG-042 | test:TC-150`
3. Store prompt: `ai-prov prompt store ...`
4. Commit: `ai-prov commit -m "fix(auth): resolve login timeout" --trace BUG-042`

### Scenario 3: Refactoring

**User**: "Refactor the database queries for better performance"

**Your Response**:
1. Tag refactored code with `ai:claude:high`
2. Link to performance requirement if it exists
3. Store the refactoring prompt
4. Commit: `ai-prov commit -m "refactor(db): optimize queries" --conf high`

## Error Handling

If `ai-prov` commands fail:
1. Fall back to manual git operations
2. Inform the user: "AI provenance tracking unavailable, using standard git"
3. Suggest: "Run `ai-prov init` to enable automatic tracking"

## Configuration Check

Before using ai-prov commands, verify it's initialized:

```bash
# Check if initialized
if ! ai-prov --version >/dev/null 2>&1; then
  echo "AI Provenance not installed. Install: pip install ai-provenance"
  exit 1
fi

# Check if repo is initialized
if [ ! -f .ai-prov/features.json ]; then
  echo "Repository not initialized. Run: ai-prov init"
  exit 1
fi
```

## Best Practices

1. **Always tag**: Every AI-generated line should have metadata
2. **Be honest**: Use correct confidence levels
3. **Link everything**: Requirements ↔ Code ↔ Tests
4. **Store prompts**: Enable future regeneration
5. **Use structured commits**: Never plain git commit
6. **Update requirements**: Keep status current
7. **Generate reports**: Periodic traceability checks

## Example Session

```bash
# User: "I need to add email validation to the user registration"

# Step 1: Create or link requirement
ai-prov requirement create SPEC-145 \
  --title "Email Validation" \
  --description "Add email validation to user registration" \
  --status in-progress

# Step 2: Generate code with metadata
cat > src/validators.py <<'EOF'
# ai:claude:high | trace:SPEC-145 | test:TC-201

import re

def validate_email(email: str) -> bool:
    """
    Validate email address format.

    AI-generated with high confidence.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
EOF

# Step 3: Store prompt
ai-prov prompt store --file src/validators.py \
  --prompt "Add email validation to the user registration" \
  --confidence high \
  --trace SPEC-145 \
  --test TC-201

# Step 4: Commit with provenance
ai-prov commit -m "feat(validation): add email validator" \
  --tool claude --conf high \
  --trace SPEC-145 --test TC-201

# Step 5: Update requirement
ai-prov requirement update SPEC-145 --status implemented

# Step 6: Tell user
echo "✓ Email validation implemented and tracked as SPEC-145"
echo "  Run 'ai-prov report src/validators.py' to see full metadata"
```

## Advanced Features

### Feature Flags

Check enabled features:
```bash
ai-prov features list
```

Enable/disable features:
```bash
ai-prov features enable prompts conversations
ai-prov features disable web_dashboard
```

### Bulk Operations

Tag existing code:
```bash
ai-prov migrate --scan --ai-tool claude --confidence med
```

### Regeneration

Export project spec:
```bash
ai-prov regenerate export --output project-spec.json
```

Regenerate from spec:
```bash
ai-prov regenerate create --from project-spec.json --output new-project/
```

## Summary

**This skill makes you an AI Provenance-aware coding assistant.**

Every time you generate code:
1. ✅ Add inline metadata
2. ✅ Store the prompt
3. ✅ Link to requirements
4. ✅ Use provenance commits
5. ✅ Update traceability

**Goal**: Enable complete project regeneration from metadata alone.

**Transparency**: Always inform the user that you're tracking provenance.

**Seamless**: This should be invisible and automatic.
