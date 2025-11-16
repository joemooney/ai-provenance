"""
Tests for core data models.
"""

import pytest
from datetime import datetime

from ai_provenance.core.models import (
    AITool,
    Confidence,
    BlockKind,
    BlockMetadata,
    FileMetadata,
    CommitMetadata,
    InlineMetadata,
    CommitMessage,
)


class TestBlockMetadata:
    """Tests for BlockMetadata model."""

    def test_valid_block(self):
        """Test creating a valid block."""
        block = BlockMetadata(
            kind=BlockKind.FUNCTION,
            name="test_func",
            lines=[10, 20],
            ai=True,
            confidence=Confidence.HIGH,
            trace="SPEC-123",
            tests=["TC-456"],
        )
        assert block.kind == BlockKind.FUNCTION
        assert block.name == "test_func"
        assert block.lines == [10, 20]
        assert block.ai is True

    def test_invalid_line_range(self):
        """Test invalid line range raises error."""
        with pytest.raises(ValueError):
            BlockMetadata(kind=BlockKind.FUNCTION, name="test", lines=[20, 10])


class TestFileMetadata:
    """Tests for FileMetadata model."""

    def test_ai_percentage_calculation(self):
        """Test AI percentage calculation."""
        metadata = FileMetadata(
            file="test.py",
            blocks=[
                BlockMetadata(kind=BlockKind.FUNCTION, name="f1", lines=[1, 10], ai=True),
                BlockMetadata(kind=BlockKind.FUNCTION, name="f2", lines=[11, 20], ai=False),
            ],
        )
        # 10 AI lines out of 20 total = 50%
        assert metadata.ai_percentage() == 50.0

    def test_empty_blocks(self):
        """Test AI percentage with no blocks."""
        metadata = FileMetadata(file="test.py")
        assert metadata.ai_percentage() == 0.0


class TestInlineMetadata:
    """Tests for inline metadata parsing."""

    def test_parse_full_metadata(self):
        """Test parsing full inline metadata."""
        comment = "# ai:claude:high | trace:SPEC-123 | test:TC-456,TC-457 | reviewed:2025-11-16:alice"
        meta = InlineMetadata.parse_comment(comment)

        assert meta is not None
        assert meta.tool == AITool.CLAUDE
        assert meta.confidence == Confidence.HIGH
        assert meta.trace == "SPEC-123"
        assert meta.tests == ["TC-456", "TC-457"]
        assert meta.reviewed == "2025-11-16:alice"

    def test_parse_minimal_metadata(self):
        """Test parsing minimal inline metadata."""
        comment = "// ai:copilot:med"
        meta = InlineMetadata.parse_comment(comment)

        assert meta is not None
        assert meta.tool == AITool.COPILOT
        assert meta.confidence == Confidence.MEDIUM

    def test_parse_invalid_comment(self):
        """Test parsing non-AI comment returns None."""
        comment = "# Just a regular comment"
        meta = InlineMetadata.parse_comment(comment)
        assert meta is None


class TestCommitMessage:
    """Tests for commit message parsing."""

    def test_parse_full_commit_message(self):
        """Test parsing full commit message with all metadata."""
        message = """[AI:claude:high] feat(auth): add JWT refresh endpoint
Trace: SPEC-89, SPEC-90
Test: TC-210, TC-211
Reviewed-by: AI+alice@example.com"""

        parsed = CommitMessage.parse(message)

        assert parsed.ai_tag == "AI:claude:high"
        assert parsed.conventional_type == "feat"
        assert parsed.scope == "auth"
        assert parsed.subject == "add JWT refresh endpoint"
        assert parsed.trace == ["SPEC-89", "SPEC-90"]
        assert parsed.tests == ["TC-210", "TC-211"]
        assert parsed.reviewed_by == "AI+alice@example.com"

    def test_parse_simple_message(self):
        """Test parsing simple message without metadata."""
        message = "fix: resolve bug"
        parsed = CommitMessage.parse(message)

        assert parsed.conventional_type == "fix"
        assert parsed.subject == "resolve bug"
        assert parsed.trace is None
        assert parsed.tests is None

    def test_parse_message_without_scope(self):
        """Test parsing conventional commit without scope."""
        message = "[AI:copilot:med] refactor: improve code quality"
        parsed = CommitMessage.parse(message)

        assert parsed.ai_tag == "AI:copilot:med"
        assert parsed.conventional_type == "refactor"
        assert parsed.scope is None
        assert parsed.subject == "improve code quality"
