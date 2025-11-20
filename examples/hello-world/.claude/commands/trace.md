# Link Code to Requirement

You are helping the user link code to a requirement for traceability.

**Instructions:**
1. Use the AskUserQuestion tool to collect:
   - Requirement ID to link to
   - What to link (file, commit, or test)
   - The path/ID to link

2. Run the appropriate ai-prov requirement link command

3. Confirm the link was created successfully

**Example:**
```bash
ai-prov requirement link SPEC-001 --file src/hello.py
ai-prov requirement link SPEC-001 --commit abc123
ai-prov requirement link SPEC-001 --test TC-001
```

Be helpful and confirm the traceability link was established.
