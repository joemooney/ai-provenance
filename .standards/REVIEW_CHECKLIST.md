# Code Review Checklist

## General

- [ ] Code follows project coding standards
- [ ] Code is self-documenting and clear
- [ ] No commented-out code (unless with explanation)
- [ ] No debug statements left in code
- [ ] Error handling is appropriate

## AI Code Specific

- [ ] All AI-generated code has inline metadata tags
- [ ] AI confidence level is appropriate
- [ ] Human review completed and documented
- [ ] AI-generated code links to requirements
- [ ] Tests exist for AI-generated code

## Functionality

- [ ] Code does what it's supposed to do
- [ ] Edge cases are handled
- [ ] Error cases are handled
- [ ] No obvious bugs
- [ ] Performance is acceptable

## Testing

- [ ] New tests added for new functionality
- [ ] Existing tests still pass
- [ ] Test coverage is adequate (>80%)
- [ ] Tests are meaningful and test the right things
- [ ] AI-generated tests reviewed for correctness

## Documentation

- [ ] Public APIs are documented
- [ ] Complex logic is explained
- [ ] README updated if needed
- [ ] REQUIREMENTS.md updated if needed
- [ ] CHANGELOG updated

## Security

- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] No hard-coded credentials
- [ ] Input validation is present
- [ ] Sensitive data is properly handled

## Requirements Traceability

- [ ] Code links to requirements (SPEC-XXX)
- [ ] Requirements are implemented correctly
- [ ] All acceptance criteria met
- [ ] Test cases cover requirements
- [ ] Traceability matrix updated

## Git & Version Control

- [ ] Commit messages are clear
- [ ] Commits are logical and atomic
- [ ] Branch name follows convention
- [ ] No merge conflicts
- [ ] AI provenance metadata in commits

## Before Merge

- [ ] All CI checks passing
- [ ] Code review approved
- [ ] AI provenance validation passed
- [ ] No unresolved comments
- [ ] Branch is up to date with main
