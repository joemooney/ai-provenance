# Coding Standards

## General Principles

1. **Clarity over cleverness**: Write code that is easy to understand
2. **Consistency**: Follow established patterns in the codebase
3. **Documentation**: Document why, not what
4. **Testing**: Write tests for all new code
5. **AI Transparency**: Tag all AI-generated code with metadata

## Language-Specific Standards

### Python

- **Style**: Follow PEP 8
- **Line length**: 100 characters
- **Imports**: Group stdlib, third-party, local
- **Docstrings**: Google style
- **Type hints**: Use for all public functions

### JavaScript/TypeScript

- **Style**: Prettier with default config
- **Semicolons**: Always use
- **Quotes**: Single quotes
- **Async**: Prefer async/await over promises

## AI Code Standards

All AI-generated code must:

1. Include inline metadata comment:
   ```python
   # ai:tool:confidence | trace:SPEC-XXX | test:TC-YYY
   ```

2. Be reviewed by a human before merging

3. Have associated test coverage

4. Link to a requirement or feature specification

## Code Review Checklist

- [ ] Code follows project conventions
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] AI code properly tagged
- [ ] No security vulnerabilities
- [ ] Performance considered
