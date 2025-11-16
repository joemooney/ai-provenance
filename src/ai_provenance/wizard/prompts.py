"""
Canned prompts for AI agents to analyze and initialize projects.

These prompts are designed to be fed to AI agents (Claude, GPT-4, etc.)
to extract project information and bootstrap AI provenance tracking.
"""

from typing import Dict, List
from pydantic import BaseModel


class PromptTemplate(BaseModel):
    """A prompt template for project initialization."""

    id: str
    name: str
    description: str
    prompt: str
    category: str
    output_format: str = "json"
    depends_on: List[str] = []  # Other prompt IDs this depends on


# ============================================================================
# PROJECT ANALYSIS PROMPTS
# ============================================================================

PROJECT_OVERVIEW_PROMPT = PromptTemplate(
    id="project_overview",
    name="Project Overview",
    description="Get high-level project information",
    category="analysis",
    prompt="""Analyze this codebase and provide a comprehensive overview.

Please examine:
1. The project's main purpose and functionality
2. Programming languages and frameworks used
3. Key dependencies and tools
4. Project structure and organization
5. Existing documentation (README, docs/, etc.)

Return a JSON object with:
{
  "name": "project name",
  "description": "brief description",
  "languages": ["python", "javascript", ...],
  "frameworks": ["django", "react", ...],
  "dependencies": {"package": "version", ...},
  "structure": "description of folder structure",
  "has_tests": true/false,
  "test_framework": "pytest/jest/etc or null",
  "build_system": "setuptools/npm/cargo/etc",
  "existing_docs": ["README.md", "docs/", ...]
}
""",
)

FEATURES_EXTRACTION_PROMPT = PromptTemplate(
    id="extract_features",
    name="Extract Features",
    description="Identify existing features and capabilities",
    category="analysis",
    depends_on=["project_overview"],
    prompt="""Based on the codebase, identify all major features and capabilities.

For each feature, extract:
1. Feature name/ID
2. Description
3. Files implementing the feature
4. Related tests (if any)
5. Current status (implemented, partial, planned)

Return a JSON array:
[
  {
    "id": "FEAT-001",
    "name": "User Authentication",
    "description": "JWT-based authentication system",
    "files": ["src/auth.py", "src/tokens.py"],
    "tests": ["tests/test_auth.py"],
    "status": "implemented",
    "estimated_complexity": "high/medium/low"
  },
  ...
]
""",
)

REQUIREMENTS_EXTRACTION_PROMPT = PromptTemplate(
    id="extract_requirements",
    name="Extract Requirements",
    description="Identify implicit requirements from code and docs",
    category="analysis",
    depends_on=["project_overview", "extract_features"],
    prompt="""Analyze the codebase and extract implicit requirements.

Look for:
1. Functional requirements (what the system does)
2. Non-functional requirements (performance, security, etc.)
3. Dependencies on external systems
4. Configuration requirements
5. Deployment requirements

For each requirement, provide:
{
  "id": "REQ-001",
  "title": "requirement title",
  "description": "detailed description",
  "type": "functional/non-functional/integration/deployment",
  "priority": "critical/high/medium/low",
  "related_features": ["FEAT-001", ...],
  "evidence": "where you found this (file, doc, comment)"
}

Return a JSON array of requirements.
""",
)

TEST_COVERAGE_PROMPT = PromptTemplate(
    id="analyze_tests",
    name="Analyze Test Coverage",
    description="Map existing tests to features",
    category="analysis",
    depends_on=["extract_features"],
    prompt="""Analyze the test suite and map tests to features.

For each test file or test case:
1. Test ID (e.g., TC-001)
2. Test name/description
3. What it tests (feature, function, class)
4. Test type (unit, integration, e2e)
5. Files/features covered

Return:
{
  "test_framework": "pytest/jest/etc",
  "total_test_files": 10,
  "tests": [
    {
      "id": "TC-001",
      "file": "tests/test_auth.py",
      "function": "test_jwt_generation",
      "type": "unit",
      "covers": ["FEAT-001"],
      "description": "Tests JWT token generation"
    },
    ...
  ],
  "coverage_gaps": [
    {"feature": "FEAT-002", "reason": "No tests found"}
  ]
}
""",
)

AI_CODE_DETECTION_PROMPT = PromptTemplate(
    id="detect_ai_code",
    name="Detect AI-Generated Code",
    description="Identify code that appears to be AI-generated",
    category="analysis",
    prompt="""Analyze the codebase for code that appears to be AI-generated.

Look for indicators:
1. Comments mentioning AI tools (Copilot, ChatGPT, Claude, etc.)
2. Very consistent formatting/style (AI pattern)
3. Detailed docstrings with examples (AI pattern)
4. Boilerplate-heavy code
5. Recent commits with unusual patterns

For each suspected AI-generated section:
{
  "file": "path/to/file.py",
  "lines": [start, end],
  "confidence": "high/medium/low",
  "indicators": ["detailed docstrings", "mentions copilot in comment"],
  "suggested_tool": "copilot/chatgpt/claude/unknown",
  "commit": "commit SHA if detectable"
}

Return a JSON array.
""",
)

DEPENDENCIES_PROMPT = PromptTemplate(
    id="analyze_dependencies",
    name="Analyze Dependencies",
    description="Extract all project dependencies",
    category="analysis",
    prompt="""Extract all project dependencies and their purposes.

Look in:
1. requirements.txt, pyproject.toml (Python)
2. package.json (JavaScript/Node)
3. Cargo.toml (Rust)
4. go.mod (Go)
5. build.gradle, pom.xml (Java)

For each dependency:
{
  "name": "package-name",
  "version": "1.2.3",
  "purpose": "why this is needed",
  "category": "runtime/dev/test/build",
  "used_in": ["list of files using it"]
}

Return:
{
  "runtime": [...],
  "dev": [...],
  "test": [...],
  "build": [...]
}
""",
)

# ============================================================================
# PROJECT STRUCTURE PROMPTS
# ============================================================================

STRUCTURE_RECOMMENDATION_PROMPT = PromptTemplate(
    id="recommend_structure",
    name="Recommend Project Structure",
    description="Suggest improvements to project organization",
    category="structure",
    depends_on=["project_overview"],
    prompt="""Based on the project type and current structure, recommend improvements.

Suggest:
1. Folder reorganization (if needed)
2. Missing directories (docs/, tests/, etc.)
3. Configuration file locations
4. Documentation structure
5. AI provenance integration points

Return:
{
  "current_structure_assessment": "good/needs-improvement/poor",
  "recommended_additions": {
    ".ai-prov/": "AI provenance data",
    "docs/requirements/": "Requirements documentation",
    "docs/architecture/": "Architecture docs",
    "tests/": "Test suite (if missing)"
  },
  "recommended_moves": {
    "old/path": "new/path"
  },
  "rationale": "explanation of recommendations"
}
""",
)

# ============================================================================
# STANDARDS & CONVENTIONS PROMPTS
# ============================================================================

CONVENTIONS_EXTRACTION_PROMPT = PromptTemplate(
    id="extract_conventions",
    name="Extract Coding Conventions",
    description="Identify existing coding standards and conventions",
    category="standards",
    prompt="""Analyze the codebase to identify coding conventions and standards.

Look for:
1. Naming conventions (camelCase, snake_case, PascalCase)
2. Code style (indentation, line length, etc.)
3. Documentation style (docstrings, comments)
4. Error handling patterns
5. Testing patterns
6. Import organization
7. File naming conventions

Return:
{
  "language": "python/javascript/etc",
  "naming": {
    "variables": "snake_case",
    "functions": "snake_case",
    "classes": "PascalCase",
    "constants": "UPPER_SNAKE_CASE"
  },
  "style": {
    "indentation": "4 spaces",
    "line_length": 100,
    "quotes": "double"
  },
  "documentation": {
    "style": "Google/NumPy/etc",
    "docstring_coverage": "80%"
  },
  "patterns": [
    "Use context managers for resources",
    "Prefer composition over inheritance"
  ]
}
""",
)

# ============================================================================
# METADATA GENERATION PROMPTS
# ============================================================================

GENERATE_REQUIREMENTS_PROMPT = PromptTemplate(
    id="generate_requirements_docs",
    name="Generate Requirements Documentation",
    description="Create formal requirements documentation from analysis",
    category="generation",
    depends_on=["extract_requirements", "extract_features"],
    prompt="""Based on the extracted requirements and features, generate formal requirements documentation.

Create a comprehensive REQUIREMENTS.md file with:
1. Functional requirements
2. Non-functional requirements
3. System requirements
4. Integration requirements
5. Traceability matrix to features

Format as markdown with clear sections and IDs.
""",
)

GENERATE_TESTS_PROMPT = PromptTemplate(
    id="generate_test_plan",
    name="Generate Test Plan",
    description="Create test plan and identify gaps",
    category="generation",
    depends_on=["analyze_tests", "extract_features"],
    prompt="""Create a comprehensive test plan.

Include:
1. Test strategy (unit, integration, e2e)
2. Test cases for each feature
3. Coverage gaps and recommendations
4. Testing procedures
5. CI/CD testing recommendations

Output as markdown TEST_PLAN.md.
""",
)

# ============================================================================
# CANNED PROMPT SETS
# ============================================================================

CANNED_PROMPTS: Dict[str, List[PromptTemplate]] = {
    "quick": [
        PROJECT_OVERVIEW_PROMPT,
        FEATURES_EXTRACTION_PROMPT,
    ],
    "standard": [
        PROJECT_OVERVIEW_PROMPT,
        FEATURES_EXTRACTION_PROMPT,
        REQUIREMENTS_EXTRACTION_PROMPT,
        TEST_COVERAGE_PROMPT,
    ],
    "comprehensive": [
        PROJECT_OVERVIEW_PROMPT,
        FEATURES_EXTRACTION_PROMPT,
        REQUIREMENTS_EXTRACTION_PROMPT,
        TEST_COVERAGE_PROMPT,
        AI_CODE_DETECTION_PROMPT,
        DEPENDENCIES_PROMPT,
        STRUCTURE_RECOMMENDATION_PROMPT,
        CONVENTIONS_EXTRACTION_PROMPT,
    ],
    "with_generation": [
        PROJECT_OVERVIEW_PROMPT,
        FEATURES_EXTRACTION_PROMPT,
        REQUIREMENTS_EXTRACTION_PROMPT,
        TEST_COVERAGE_PROMPT,
        STRUCTURE_RECOMMENDATION_PROMPT,
        GENERATE_REQUIREMENTS_PROMPT,
        GENERATE_TESTS_PROMPT,
    ],
}

# All available prompts
ALL_PROMPTS = [
    PROJECT_OVERVIEW_PROMPT,
    FEATURES_EXTRACTION_PROMPT,
    REQUIREMENTS_EXTRACTION_PROMPT,
    TEST_COVERAGE_PROMPT,
    AI_CODE_DETECTION_PROMPT,
    DEPENDENCIES_PROMPT,
    STRUCTURE_RECOMMENDATION_PROMPT,
    CONVENTIONS_EXTRACTION_PROMPT,
    GENERATE_REQUIREMENTS_PROMPT,
    GENERATE_TESTS_PROMPT,
]
