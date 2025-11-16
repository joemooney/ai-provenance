# FEAT-001: Core Metadata Tracking

## Overview

Implement core AI provenance metadata tracking at multiple hierarchical levels.

## Requirements

- Line-level metadata via inline comments
- Block/function-level metadata
- File-level metadata with .meta.json files
- Commit-level metadata via git notes

## Implementation

**Files:**
- `src/ai_provenance/core/models.py`
- `src/ai_provenance/parsers/stamper.py`
- `src/ai_provenance/git_integration/notes.py`

**Status:** Implemented

## Test Cases

- TC-001: Test inline metadata parsing
- TC-002: Test file metadata generation
- TC-003: Test git notes CRUD operations

## Acceptance Criteria

- [x] Parse inline metadata from multiple comment styles
- [x] Store metadata in Pydantic models
- [x] Git notes integration working
- [x] Language-agnostic support
