"""
AI Provenance - Git-native AI code provenance and metadata tracking system.
"""

__version__ = "0.1.0"
__author__ = "AI Provenance Contributors"
__license__ = "MIT"

from ai_provenance.core.models import (
    AITool,
    Confidence,
    BlockMetadata,
    FileMetadata,
    CommitMetadata,
)

__all__ = [
    "AITool",
    "Confidence",
    "BlockMetadata",
    "FileMetadata",
    "CommitMetadata",
]
