# Create AI Provenance Requirement

You are helping the user create a new requirement for AI Provenance tracking.

**Instructions:**
1. Use the AskUserQuestion tool to collect the following information:
   - Requirement ID (e.g., SPEC-001, SPEC-002)
   - Title (brief summary)
   - Description (detailed description)
   - Type (feature, bug, enhancement, documentation)
   - Priority (critical, high, medium, low)

2. After collecting the information, run the ai-prov requirement create command with the collected data

3. Show the user the created requirement and ask if they want to create another one

**Example:**
```bash
ai-prov requirement create SPEC-001 \
  --title "Hello World Program" \
  --description "Create a simple program that greets the user" \
  --type feature \
  --priority high
```

Be friendly and guide the user through the process step by step.
