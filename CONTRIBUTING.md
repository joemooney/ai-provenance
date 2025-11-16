# Contributing to AI Provenance

Thank you for your interest in contributing to AI Provenance! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/ai-provenance/ai-provenance/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)

### Suggesting Features

1. Check existing feature requests
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Potential implementation approach

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Format code (`black src tests`)
7. Commit with provenance metadata:
   ```bash
   git commit -m "[AI:tool:conf] feat: add new feature
   Trace: FEATURE-123
   Test: TC-456
   Reviewed-by: AI+your.email@example.com"
   ```
8. Push to your fork
9. Create a Pull Request

### Development Setup

```bash
# Clone repository
git clone https://github.com/ai-provenance/ai-provenance
cd ai-provenance

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Initialize AI provenance
ai-prov init

# Run tests
pytest

# Format code
black src tests
ruff check src tests
```

### Coding Standards

- Follow PEP 8
- Use type hints
- Write docstrings for all public functions/classes
- Keep functions small and focused
- Add tests for new features

### Commit Messages

Use conventional commit format with AI provenance:

```
[AI:tool:conf] type(scope): subject

Body (optional)

Trace: SPEC-xxx
Test: TC-xxx
Reviewed-by: AI+email@example.com
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

### AI-Generated Code Guidelines

1. **Always tag AI code**:
   ```python
   # ai:claude:high | trace:SPEC-123 | test:TC-456 | reviewed:2025-11-16:alice
   def my_function():
       pass
   ```

2. **Review requirement**: All AI code must be reviewed by a human

3. **Test coverage**: AI-generated features must have tests

4. **Confidence levels**:
   - `high`: Copy-pasted with minor edits
   - `med`: Significant modifications
   - `low`: AI-assisted but mostly human

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ai_provenance --cov-report=html

# Run specific test file
pytest tests/test_core.py

# Run specific test
pytest tests/test_core.py::test_metadata_parsing
```

### Documentation

- Update README.md for user-facing changes
- Add docstrings to new code
- Update examples if needed
- Add to CHANGELOG.md

### Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create git tag: `git tag -a v0.2.0 -m "Release v0.2.0"`
4. Push tag: `git push origin v0.2.0`
5. GitHub Actions will build and publish to PyPI

## Questions?

Open a [Discussion](https://github.com/ai-provenance/ai-provenance/discussions) or reach out via Issues.

Thank you for contributing! 🚀
