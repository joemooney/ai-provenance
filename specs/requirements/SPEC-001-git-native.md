# SPEC-001: Git-Native Storage

## Requirement

All AI provenance metadata must be stored using Git-native mechanisms with no external dependencies.

## Rationale

- **Portability**: Metadata travels with `git clone`
- **Immutability**: Git's cryptographic hashing ensures tamper-evidence
- **Offline capability**: Works without internet
- **Zero lock-in**: No proprietary formats or databases

## Implementation

### Storage Mechanisms

1. **Git Notes** (`refs/notes/ai-provenance`)
   - Immutable commit-level metadata
   - JSON payload with AI tool, confidence, traces, tests

2. **Inline Comments**
   - Line/block-level metadata
   - Language-agnostic comment detection
   - Format: `# ai:tool:conf | trace:XXX | test:YYY`

3. **Committed Files** (`.ai-prov/` directory)
   - Requirements database
   - Prompts and conversations
   - Traceability links
   - Feature configuration

4. **Git Attributes** (`.gitattributes`)
   - Filter driver configuration
   - File type handling

## Constraints

- Must work with Git 2.20+
- No external database dependencies
- All data in repository
- Standard JSON format for metadata

## Success Criteria

- [x] Git notes working
- [x] Inline metadata parseable
- [x] .ai-prov/ directory structure defined
- [x] No external dependencies required
