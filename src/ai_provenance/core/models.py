"""
Core data models for AI provenance metadata.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class AITool(str, Enum):
    """Supported AI tools."""

    CLAUDE = "claude"
    COPILOT = "copilot"
    CHATGPT = "chatgpt"
    GEMINI = "gemini"
    CURSOR = "cursor"
    OTHER = "other"


class Confidence(str, Enum):
    """Confidence level for AI-generated code."""

    HIGH = "high"  # Copy-pasted with minor edits
    MEDIUM = "med"  # Significant modifications
    LOW = "low"  # AI-assisted but mostly human-written


class BlockKind(str, Enum):
    """Type of code block."""

    FUNCTION = "function"
    METHOD = "method"
    CLASS = "class"
    BLOCK = "block"
    MODULE = "module"


class BlockMetadata(BaseModel):
    """Metadata for a code block (function, class, method, etc.)."""

    kind: BlockKind
    name: str
    lines: List[int] = Field(min_length=2, max_length=2, description="[start, end] line numbers")
    ai: bool = False
    confidence: Optional[Confidence] = None
    trace: Optional[str] = Field(None, description="Requirement ID (e.g., SPEC-123)")
    tests: Optional[List[str]] = Field(None, description="Test case IDs (e.g., TC-456)")

    @field_validator("lines")
    @classmethod
    def validate_lines(cls, v: List[int]) -> List[int]:
        """Ensure line range is valid."""
        if len(v) != 2:
            raise ValueError("lines must be [start, end]")
        if v[0] < 1 or v[1] < v[0]:
            raise ValueError("Invalid line range")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "kind": "function",
                "name": "refresh_token",
                "lines": [42, 68],
                "ai": True,
                "confidence": "high",
                "trace": "SPEC-89",
                "tests": ["TC-210"],
            }
        }


class FileMetadata(BaseModel):
    """Metadata for an entire file."""

    file: str = Field(description="Relative path to the file")
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    ai_tool: Optional[AITool] = None
    confidence: Optional[Confidence] = None
    trace: Optional[List[str]] = Field(None, description="Requirement IDs")
    tests: Optional[List[str]] = Field(None, description="Test case IDs")
    reviewed_by: Optional[str] = Field(None, description="Reviewer email")
    reviewed_at: Optional[datetime] = None
    blocks: List[BlockMetadata] = Field(default_factory=list)

    def ai_percentage(self) -> float:
        """Calculate percentage of AI-generated lines."""
        if not self.blocks:
            return 0.0

        total_lines = 0
        ai_lines = 0

        for block in self.blocks:
            block_lines = block.lines[1] - block.lines[0] + 1
            total_lines += block_lines
            if block.ai:
                ai_lines += block_lines

        return (ai_lines / total_lines * 100) if total_lines > 0 else 0.0

    class Config:
        json_schema_extra = {
            "example": {
                "file": "src/auth.py",
                "generated_at": "2025-11-16T13:38:00Z",
                "ai_tool": "claude",
                "confidence": "high",
                "trace": ["SPEC-89"],
                "tests": ["TC-210", "TC-211"],
                "reviewed_by": "alice@example.com",
                "blocks": [
                    {
                        "kind": "function",
                        "name": "refresh_token",
                        "lines": [42, 68],
                        "ai": True,
                        "confidence": "high",
                    }
                ],
            }
        }


class CommitMetadata(BaseModel):
    """Metadata stored in git notes for a commit."""

    ai_tool: Optional[AITool] = None
    confidence: Optional[Confidence] = None
    trace: Optional[List[str]] = Field(None, description="Requirement IDs")
    tests: Optional[List[str]] = Field(None, description="Test case IDs")
    reviewed_by: Optional[str] = Field(None, description="Reviewer email")
    reviewed_at: Optional[datetime] = None
    files: Optional[List[str]] = Field(None, description="Files affected")

    class Config:
        json_schema_extra = {
            "example": {
                "ai_tool": "claude",
                "confidence": "high",
                "trace": ["SPEC-89"],
                "tests": ["TC-210"],
                "reviewed_by": "alice@example.com",
                "reviewed_at": "2025-11-16T14:00:00Z",
                "files": ["src/auth.py"],
            }
        }


class InlineMetadata(BaseModel):
    """Metadata extracted from inline comments."""

    tool: Optional[AITool] = None
    confidence: Optional[Confidence] = None
    trace: Optional[str] = None
    tests: Optional[List[str]] = None
    reviewed: Optional[str] = None  # "YYYY-MM-DD:reviewer"
    line_number: Optional[int] = None

    @classmethod
    def parse_comment(cls, comment: str) -> Optional["InlineMetadata"]:
        """
        Parse inline metadata comment.

        Format: ai:tool:conf | trace:SPEC-123 | test:TC-456 | reviewed:YYYY-MM-DD:name

        Examples:
            # ai:claude:high | trace:SPEC-89 | test:TC-210
            // ai:copilot:med | reviewed:2025-11-16:alice
        """
        # Remove comment markers
        clean = comment.strip()
        for marker in ["#", "//", "/*", "*/"]:
            clean = clean.replace(marker, "")
        clean = clean.strip()

        if not clean.startswith("ai:"):
            return None

        metadata: dict = {}
        parts = [p.strip() for p in clean.split("|")]

        for part in parts:
            if part.startswith("ai:"):
                # Parse ai:tool:conf
                ai_parts = part.split(":")
                if len(ai_parts) >= 2:
                    try:
                        metadata["tool"] = AITool(ai_parts[1])
                    except ValueError:
                        metadata["tool"] = AITool.OTHER
                if len(ai_parts) >= 3:
                    try:
                        metadata["confidence"] = Confidence(ai_parts[2])
                    except ValueError:
                        pass

            elif ":" in part:
                key, value = part.split(":", 1)
                key = key.strip()
                value = value.strip()

                if key == "trace":
                    metadata["trace"] = value
                elif key == "test":
                    metadata["tests"] = [t.strip() for t in value.split(",")]
                elif key == "reviewed":
                    metadata["reviewed"] = value

        return cls(**metadata) if metadata else None


class CommitMessage(BaseModel):
    """Parsed commit message with provenance metadata."""

    raw: str
    ai_tag: Optional[str] = None  # [AI:claude:high]
    conventional_type: Optional[str] = None  # feat, fix, refactor, etc.
    scope: Optional[str] = None
    subject: str
    trace: Optional[List[str]] = None
    tests: Optional[List[str]] = None
    reviewed_by: Optional[str] = None

    @classmethod
    def parse(cls, message: str) -> "CommitMessage":
        """
        Parse commit message according to convention.

        Format:
            [AI:tool:conf] type(scope): subject
            Trace: SPEC-123, SPEC-456
            Test: TC-789
            Reviewed-by: AI+alice@example.com
        """
        lines = message.strip().split("\n")
        first_line = lines[0] if lines else ""

        data: dict = {"raw": message, "subject": first_line}

        # Parse AI tag
        if first_line.startswith("[AI:"):
            ai_end = first_line.find("]")
            if ai_end > 0:
                data["ai_tag"] = first_line[1:ai_end]
                first_line = first_line[ai_end + 1 :].strip()

        # Parse conventional commit type(scope): subject
        if ":" in first_line:
            prefix, subject = first_line.split(":", 1)
            data["subject"] = subject.strip()

            if "(" in prefix and ")" in prefix:
                conv_type, rest = prefix.split("(", 1)
                scope = rest.split(")", 1)[0]
                data["conventional_type"] = conv_type.strip()
                data["scope"] = scope.strip()
            else:
                data["conventional_type"] = prefix.strip()

        # Parse body metadata
        for line in lines[1:]:
            line = line.strip()
            if line.startswith("Trace:"):
                trace_str = line[6:].strip()
                data["trace"] = [t.strip() for t in trace_str.split(",")]
            elif line.startswith("Test:"):
                test_str = line[5:].strip()
                data["tests"] = [t.strip() for t in test_str.split(",")]
            elif line.startswith("Reviewed-by:"):
                data["reviewed_by"] = line[12:].strip()

        return cls(**data)
