# Stamp AI Metadata on Code

You are helping the user add AI provenance metadata to a code file.

**Instructions:**
1. Use the AskUserQuestion tool to collect:
   - File path to stamp
   - AI tool used (claude, copilot, chatgpt, etc.)
   - Confidence level (high, med, low)
   - Optional: Requirement IDs (trace)
   - Optional: Test case IDs (test)
   - Optional: Reviewer email

2. Run the ai-prov stamp command with the collected data

3. Show the user the stamped file and confirm success

**Example:**
```bash
ai-prov stamp src/auth.py \
  --tool claude \
  --conf high \
  --trace SPEC-089 \
  --test TC-210 \
  --reviewer alice@example.com
```

Guide the user through adding provenance metadata to their AI-generated code.
