"""
Data models for prompts and conversations.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from uuid import uuid4

from pydantic import BaseModel, Field


class PromptType(str, Enum):
    """Type of prompt."""

    CODE_GENERATION = "code_generation"
    CODE_MODIFICATION = "code_modification"
    DEBUGGING = "debugging"
    REFACTORING = "refactoring"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    EXPLANATION = "explanation"
    PLANNING = "planning"


class MessageRole(str, Enum):
    """Role in a conversation."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Prompt(BaseModel):
    """A prompt used to generate code."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Prompt content
    prompt_text: str
    prompt_type: PromptType = PromptType.CODE_GENERATION
    context: List[str] = Field(
        default_factory=list, description="Previous messages or context"
    )

    # AI metadata
    ai_tool: str = "claude"
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None

    # Response
    response_summary: Optional[str] = None
    response_full: Optional[str] = None  # Optional: full AI response
    confidence: str = "high"  # high, med, low

    # Code metadata
    files_created: List[str] = Field(default_factory=list)
    files_modified: List[str] = Field(default_factory=list)
    lines_generated: Optional[tuple[int, int]] = None  # (start, end)

    # Traceability
    requirement_ids: List[str] = Field(default_factory=list)
    test_ids: List[str] = Field(default_factory=list)
    commit_sha: Optional[str] = None

    # Conversation link
    conversation_id: Optional[str] = None
    message_index: Optional[int] = None

    # Metadata
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "prompt_text": "Create a JWT authentication function with refresh tokens",
                "prompt_type": "code_generation",
                "ai_tool": "claude",
                "response_summary": "Generated refresh_token() function with error handling",
                "files_created": ["src/auth.py"],
                "lines_generated": [42, 68],
                "requirement_ids": ["SPEC-089"],
                "test_ids": ["TC-210"],
                "confidence": "high",
            }
        }


class ConversationMessage(BaseModel):
    """A single message in a conversation."""

    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    prompt_id: Optional[str] = None  # Link to Prompt if this generated code
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Conversation(BaseModel):
    """A full conversation with an AI assistant."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None

    # Conversation details
    title: Optional[str] = None
    description: Optional[str] = None
    ai_tool: str = "claude"
    model: Optional[str] = None

    # Messages
    messages: List[ConversationMessage] = Field(default_factory=list)

    # Outcomes
    files_created: List[str] = Field(default_factory=list)
    files_modified: List[str] = Field(default_factory=list)
    commits: List[str] = Field(default_factory=list)

    # Traceability
    requirement_ids: List[str] = Field(default_factory=list)
    test_ids: List[str] = Field(default_factory=list)
    prompts: List[str] = Field(default_factory=list, description="Prompt IDs")

    # Metadata
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # Session info
    session_id: Optional[str] = None
    user: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Implement OAuth2 Authentication",
                "ai_tool": "claude",
                "messages": [
                    {
                        "role": "user",
                        "content": "I need to implement OAuth2 authentication",
                    },
                    {
                        "role": "assistant",
                        "content": "I'll help you implement OAuth2. Let's start with...",
                    },
                ],
                "files_created": ["src/oauth.py", "src/tokens.py"],
                "requirement_ids": ["SPEC-089"],
                "prompts": ["prompt-uuid-1", "prompt-uuid-2"],
            }
        }


class ProjectSpec(BaseModel):
    """Complete project specification for regeneration."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: str
    version: str = "1.0.0"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Requirements
    requirements: List[str] = Field(
        default_factory=list, description="Requirement IDs"
    )

    # All prompts used
    prompts: List[str] = Field(default_factory=list, description="Prompt IDs")

    # All conversations
    conversations: List[str] = Field(
        default_factory=list, description="Conversation IDs"
    )

    # Files and structure
    file_structure: Dict[str, Any] = Field(
        default_factory=dict, description="Directory tree"
    )
    files: Dict[str, str] = Field(
        default_factory=dict, description="File path -> content hash"
    )

    # Dependencies
    dependencies: Dict[str, str] = Field(
        default_factory=dict, description="Package -> version"
    )

    # Git metadata
    git_commits: List[str] = Field(default_factory=list)
    git_branches: List[str] = Field(default_factory=list)

    # AI metadata
    ai_tools_used: List[str] = Field(default_factory=list)
    ai_percentage: float = 0.0

    # Metadata
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
