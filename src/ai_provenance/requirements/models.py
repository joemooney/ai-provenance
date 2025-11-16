"""
Requirements management data models.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field


class RequirementStatus(str, Enum):
    """Status of a requirement."""

    PLANNED = "planned"
    IN_PROGRESS = "in-progress"
    IMPLEMENTED = "implemented"
    TESTED = "tested"
    VERIFIED = "verified"
    DEPRECATED = "deprecated"


class RequirementType(str, Enum):
    """Type of requirement."""

    FEATURE = "feature"
    BUG = "bug"
    ENHANCEMENT = "enhancement"
    REFACTOR = "refactor"
    DOCUMENTATION = "documentation"
    TEST = "test"
    SPIKE = "spike"  # Research/investigation


class RequirementPriority(str, Enum):
    """Priority level."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Requirement(BaseModel):
    """A single requirement or specification."""

    id: str = Field(description="Unique identifier (e.g., SPEC-001, FEAT-042)")
    title: str
    description: str
    type: RequirementType = RequirementType.FEATURE
    status: RequirementStatus = RequirementStatus.PLANNED
    priority: RequirementPriority = RequirementPriority.MEDIUM

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
    assigned_to: Optional[str] = None

    # Traceability
    parent: Optional[str] = Field(None, description="Parent requirement ID")
    children: List[str] = Field(default_factory=list, description="Child requirement IDs")
    related: List[str] = Field(default_factory=list, description="Related requirement IDs")

    # Implementation links
    files: List[str] = Field(default_factory=list, description="Files implementing this")
    commits: List[str] = Field(default_factory=list, description="Commits for this requirement")
    tests: List[str] = Field(default_factory=list, description="Test case IDs")

    # AI metadata
    ai_generated: bool = False
    ai_tool: Optional[str] = None
    prompts: List[str] = Field(default_factory=list, description="Prompt IDs used")

    # Custom fields
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # Acceptance criteria
    acceptance_criteria: List[str] = Field(default_factory=list)

    # External links
    external_links: Dict[str, str] = Field(
        default_factory=dict, description="Links to external systems (Jira, GitHub, etc.)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "SPEC-089",
                "title": "JWT Authentication System",
                "description": "Implement JWT-based authentication with refresh tokens",
                "type": "feature",
                "status": "implemented",
                "priority": "high",
                "files": ["src/auth.py", "src/tokens.py"],
                "commits": ["abc123", "def456"],
                "tests": ["TC-210", "TC-211"],
                "ai_generated": True,
                "ai_tool": "claude",
                "acceptance_criteria": [
                    "Users can login with email/password",
                    "JWT tokens expire after 1 hour",
                    "Refresh tokens valid for 7 days",
                ],
            }
        }


class TestCase(BaseModel):
    """A test case linked to requirements."""

    id: str = Field(description="Unique test case ID (e.g., TC-001)")
    title: str
    description: str
    requirement_ids: List[str] = Field(default_factory=list)

    # Test details
    test_type: str = Field(default="unit", description="unit, integration, e2e, etc.")
    file: Optional[str] = Field(None, description="Test file location")
    function: Optional[str] = Field(None, description="Test function name")

    # Status
    status: str = Field(default="pending", description="pending, passing, failing")
    last_run: Optional[datetime] = None
    last_result: Optional[str] = None

    # AI metadata
    ai_generated: bool = False
    ai_tool: Optional[str] = None

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    tags: List[str] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "TC-210",
                "title": "Test JWT token generation",
                "description": "Verify that JWT tokens are generated correctly",
                "requirement_ids": ["SPEC-089"],
                "test_type": "unit",
                "file": "tests/test_auth.py",
                "function": "test_jwt_generation",
                "status": "passing",
                "ai_generated": True,
                "ai_tool": "claude",
            }
        }


class TraceLink(BaseModel):
    """Bidirectional traceability link."""

    source_type: str  # requirement, code, test, prompt
    source_id: str
    target_type: str
    target_id: str
    link_type: str = "implements"  # implements, tests, relates_to, depends_on
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
