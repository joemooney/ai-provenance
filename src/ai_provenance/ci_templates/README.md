# CI/CD Integration Templates

This directory contains ready-to-use CI/CD templates for AI provenance validation.

## GitHub Actions

Copy `github-actions.yml` to `.github/workflows/ai-provenance.yml` in your repository:

```bash
mkdir -p .github/workflows
cp github-actions.yml .github/workflows/ai-provenance.yml
git add .github/workflows/ai-provenance.yml
git commit -m "ci: add AI provenance validation"
```

### What it does:

- ✅ Validates all AI commits have proper metadata
- ✅ Checks for required reviews
- ✅ Verifies test coverage for traced features
- ✅ Generates AI % metrics for PRs
- ✅ Comments on PRs with provenance report
- ✅ Creates traceability matrix
- ✅ Checks for unreviewed AI code

### Customization:

```yaml
# Disable review requirement
ai-prov validate --require-tests

# Change Python version
python-version: '3.10'

# Run on different branches
branches: [main, develop, staging]
```

## GitLab CI

Add the contents of `gitlab-ci.yml` to your `.gitlab-ci.yml`:

```bash
cat gitlab-ci.yml >> .gitlab-ci.yml
git add .gitlab-ci.yml
git commit -m "ci: add AI provenance validation"
```

### What it does:

- ✅ Validates repository metadata
- ✅ Generates metrics and reports
- ✅ Creates artifacts for download
- ✅ Posts MR comments with provenance info
- ✅ Generates traceability matrix

### Customization:

```yaml
# Use different Python version
image: python:3.10

# Change artifact expiration
expire_in: 7 days

# Disable MR comments
rules:
  - when: never
```

## Pre-commit Hook

For local validation before pushing:

```bash
# Install pre-commit
pip install pre-commit

# Add to .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: ai-provenance
        name: AI Provenance Validation
        entry: ai-prov validate --require-review
        language: system
        pass_filenames: false
```

## Jenkins Pipeline

Example Jenkinsfile snippet:

```groovy
stage('AI Provenance') {
    steps {
        sh 'pip install ai-provenance'
        sh 'ai-prov validate --require-review --require-tests'
        sh 'ai-prov query --ai-percent --by-file > metrics.txt'
        archiveArtifacts artifacts: 'metrics.txt'
    }
}
```

## CircleCI

Example `.circleci/config.yml` snippet:

```yaml
jobs:
  ai-provenance:
    docker:
      - image: python:3.11
    steps:
      - checkout
      - run:
          name: Install AI Provenance
          command: pip install ai-provenance
      - run:
          name: Validate Repository
          command: ai-prov validate --require-review --require-tests
      - run:
          name: Generate Metrics
          command: ai-prov query --ai-percent > metrics.txt
      - store_artifacts:
          path: metrics.txt
```

## Azure Pipelines

Example `azure-pipelines.yml` snippet:

```yaml
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.11'

- script: |
    pip install ai-provenance
    ai-prov validate --require-review --require-tests
    ai-prov query --ai-percent > $(Build.ArtifactStagingDirectory)/metrics.txt
  displayName: 'AI Provenance Validation'

- task: PublishBuildArtifacts@1
  inputs:
    pathToPublish: '$(Build.ArtifactStagingDirectory)/metrics.txt'
    artifactName: 'ai-provenance-metrics'
```

## Required Secrets/Variables

Most integrations don't require additional secrets, but for MR/PR comments you may need:

- **GitHub**: `GITHUB_TOKEN` (automatically provided)
- **GitLab**: `CI_JOB_TOKEN` (automatically provided)

## Customizing Validation Rules

Adjust validation strictness:

```bash
# Require only reviews
ai-prov validate --require-review

# Require only tests
ai-prov validate --require-tests

# No requirements (just check format)
ai-prov validate

# Custom checks in CI script
if ai-prov query --unreviewed | grep -q "Found"; then
  echo "Unreviewed AI code detected!"
  exit 1
fi
```

## Best Practices

1. **Start Permissive**: Begin with warnings, then enforce over time
2. **Review Required**: Always require human review for AI code
3. **Test Coverage**: Link AI code to test cases for traceability
4. **Metrics Tracking**: Archive metrics artifacts for trend analysis
5. **Documentation**: Include provenance reports in release notes

## Troubleshooting

### "ai-prov command not found"

Ensure `ai-provenance` is installed in the CI environment:

```bash
pip install ai-provenance
```

### "Not a git repository"

Ensure full git history is checked out:

```yaml
# GitHub Actions
with:
  fetch-depth: 0

# GitLab CI
variables:
  GIT_DEPTH: 0
```

### "Permission denied" on hooks

Hooks are installed automatically during `ai-prov init`. If they fail:

```bash
chmod +x .git/hooks/*
```

### Git notes not pushed

Ensure notes are pushed with commits:

```bash
git push origin refs/notes/ai-provenance
```

Or configure automatic pushing:

```bash
git config remote.origin.push '+refs/notes/ai-provenance:refs/notes/ai-provenance'
```
