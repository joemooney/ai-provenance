# AI Provenance - Project Overview

## Vision

Create the definitive, Git-native solution for tracking, attributing, and auditing AI-generated code. Enable developers, teams, and organizations to understand AI's contribution to their codebases with full traceability, transparency, and compliance.

## General Information

**AI Provenance** is an open-source tool that extends Git with AI code provenance capabilities. It answers critical questions:

- **What % of my code is AI-generated?**
- **Which commits contain AI code?**
- **Has all AI code been reviewed by humans?**
- **Which requirements are implemented with AI?**
- **What test coverage exists for AI-generated code?**
- **Can I audit AI contributions over time?**

## Problem Statement

As AI coding assistants (Copilot, Claude, ChatGPT, etc.) become ubiquitous, organizations need:

1. **Attribution**: Know what code came from AI
2. **Review processes**: Ensure human oversight of AI code
3. **Compliance**: Meet regulatory requirements for AI-generated software
4. **Quality control**: Link AI code to requirements and tests
5. **Audit trails**: Historical record of AI contributions

Existing solutions either:
- Require expensive SaaS platforms
- Don't integrate with Git
- Lack language support
- Can't track historical metadata

## Solution

AI Provenance provides:

### Core Features

1. **Hierarchical Metadata**
   - Line-level: Inline comments with AI tags
   - Block-level: Function/class attribution
   - File-level: `.meta.json` files
   - Commit-level: Git notes with immutable records

2. **Commit Conventions**
   - Machine-parsable format: `[AI:tool:conf] type(scope): subject`
   - Automatic validation via git hooks
   - Links to requirements (Trace:) and tests (Test:)

3. **Traceability**
   - Requirement → Code → Test mapping
   - Review tracking
   - Confidence levels (high/med/low)

4. **Reporting**
   - AI % metrics by file/repo
   - Unreviewed code detection
   - Traceability matrices
   - Historical analysis

5. **CI/CD Integration**
   - GitHub Actions templates
   - GitLab CI pipelines
   - Validation gates
   - Automated PR comments

### Technical Approach

- **Git-native**: All data stored in Git (no external DBs)
- **Language-agnostic**: Works with any text-based code
- **Zero-config**: Works out of the box
- **Offline-capable**: No cloud dependencies
- **Temporal**: Full historical reconstruction

## Use Cases

### Individual Developers

Track personal AI usage, improve prompting, understand AI contribution to projects.

```bash
ai-prov query --ai-percent --by-file
ai-prov report src/main.py
```

### Development Teams

Enforce review policies, ensure test coverage, maintain code quality.

```bash
ai-prov validate --require-review --require-tests
ai-prov query --unreviewed
```

### Enterprise Organizations

Compliance, audit trails, regulatory requirements, IP management.

```bash
ai-prov trace-matrix --format html > audit-report.html
ai-prov report --format json > metrics.json
```

### Researchers

Analyze AI coding patterns, study AI effectiveness, publish metrics.

```bash
# Track AI % over time
git log --oneline | while read sha _; do
  ai-prov report --rev $sha > reports/$sha.txt
done
```

## Architecture Principles

1. **Immutability**: Git notes provide tamper-proof records
2. **Portability**: All metadata travels with `git clone`
3. **Simplicity**: Plain text, JSON, standard Git operations
4. **Extensibility**: Plugin architecture for new AI tools
5. **Privacy**: No data leaves your repository

## Workflow

```
┌─────────────────┐
│  Write Code     │
│  (AI-assisted)  │
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Stamp Metadata │
│  ai-prov stamp  │
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Human Review   │
│  + Update tag   │
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Commit         │
│  ai-prov commit │
└────────┬────────┘
         │
         v
┌─────────────────┐
│  CI Validation  │
│  GitHub Actions │
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Reports/Audit  │
│  Traceability   │
└─────────────────┘
```

## Target Audience

- **Developers**: Anyone using AI coding assistants
- **Tech Leads**: Need visibility into AI usage
- **QA Teams**: Validate AI code quality
- **Compliance Officers**: Audit requirements
- **Security Teams**: Track code provenance
- **Researchers**: Study AI-assisted development

## Competitive Advantages

| Feature | AI Provenance | Traditional VCS | SaaS Tools |
|---------|---------------|-----------------|------------|
| Git-native | ✅ | ❌ | ❌ |
| Language-agnostic | ✅ | ❌ | ⚠️ |
| Zero external deps | ✅ | ✅ | ❌ |
| Temporal coverage | ✅ | ❌ | ⚠️ |
| Open source | ✅ | ✅ | ❌ |
| Offline capable | ✅ | ✅ | ❌ |
| CI/CD ready | ✅ | ❌ | ✅ |

## Distribution

- **PyPI**: `pip install ai-provenance`
- **GitHub**: Source code and releases
- **Docker**: (Planned) Container images
- **Homebrew**: (Planned) macOS/Linux packages

## Roadmap

### Phase 1: Core (Current)
- ✅ CLI tool
- ✅ Git integration
- ✅ Basic reporting
- ✅ CI/CD templates

### Phase 2: Enhanced Tracking
- 🔲 Filter driver for auto .meta.json
- 🔲 Tree-sitter integration
- 🔲 Diff analysis for AI % over time
- 🔲 Advanced hunk detection

### Phase 3: Visualization
- 🔲 Web dashboard
- 🔲 IDE integration (VS Code)
- 🔲 Charts and graphs
- 🔲 Export to CSV/Excel

### Phase 4: Enterprise
- 🔲 SAML/SSO integration
- 🔲 Policy enforcement
- 🔲 Advanced compliance features
- 🔲 Multi-repo aggregation

## Community & Support

- **Documentation**: https://ai-provenance.readthedocs.io (planned)
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Contributing**: See CONTRIBUTING.md
- **License**: MIT

## Getting Started

```bash
# Install
pip install ai-provenance

# Initialize
cd your-project
ai-prov init

# Tag AI code
ai-prov stamp src/file.py --tool claude --conf high

# Commit
ai-prov commit -m "feat: add feature" --tool claude --conf high

# Report
ai-prov query --ai-percent
ai-prov trace-matrix
```

## Key Differentiators

1. **Git as the database**: No external storage needed
2. **Language flexibility**: Any comment style works
3. **Time machine**: Reconstruct metadata for any commit
4. **Zero lock-in**: All data is in your repo
5. **CI/CD first**: Built for automation

## Success Metrics

- **Adoption**: PyPI downloads, GitHub stars
- **Coverage**: % of AI code tracked in projects
- **Quality**: Issues closed, tests passing
- **Community**: Contributors, discussions
- **Impact**: Papers published, case studies

## Project Values

- **Transparency**: Open source, no hidden behavior
- **Privacy**: Your code stays yours
- **Simplicity**: Easy to use, easy to understand
- **Reliability**: Works offline, no dependencies
- **Community**: Built by developers, for developers
