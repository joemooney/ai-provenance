"""
Prompt and conversation storage.
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from ai_provenance.prompts.models import (
    Prompt,
    Conversation,
    ConversationMessage,
    MessageRole,
    ProjectSpec,
)


class PromptStore:
    """Store and retrieve prompts."""

    def __init__(self, repo_path: Optional[str] = None):
        """Initialize prompt store."""
        if repo_path is None:
            repo_path = "."

        self.repo_path = Path(repo_path)
        self.prompts_dir = self.repo_path / ".ai-prov" / "prompts"
        self.prompts_dir.mkdir(parents=True, exist_ok=True)

    def store(self, prompt: Prompt) -> str:
        """Store a prompt and return its ID."""
        prompt_file = self.prompts_dir / f"{prompt.id}.json"
        prompt_file.write_text(prompt.model_dump_json(indent=2))
        return prompt.id

    def get(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by ID."""
        prompt_file = self.prompts_dir / f"{prompt_id}.json"

        if not prompt_file.exists():
            return None

        data = json.loads(prompt_file.read_text())
        return Prompt(**data)

    def list_for_file(self, file_path: str) -> List[Prompt]:
        """List all prompts that generated or modified a file."""
        prompts = []

        for prompt_file in self.prompts_dir.glob("*.json"):
            data = json.loads(prompt_file.read_text())
            prompt = Prompt(**data)

            if file_path in prompt.files_created or file_path in prompt.files_modified:
                prompts.append(prompt)

        # Sort by timestamp
        return sorted(prompts, key=lambda p: p.timestamp)

    def list_for_requirement(self, req_id: str) -> List[Prompt]:
        """List all prompts for a requirement."""
        prompts = []

        for prompt_file in self.prompts_dir.glob("*.json"):
            data = json.loads(prompt_file.read_text())
            prompt = Prompt(**data)

            if req_id in prompt.requirement_ids:
                prompts.append(prompt)

        return sorted(prompts, key=lambda p: p.timestamp)

    def create_from_text(
        self,
        prompt_text: str,
        file_path: Optional[str] = None,
        requirement_ids: Optional[List[str]] = None,
        **kwargs,
    ) -> Prompt:
        """Create and store a prompt from text."""
        prompt = Prompt(
            prompt_text=prompt_text,
            files_modified=[file_path] if file_path else [],
            requirement_ids=requirement_ids or [],
            **kwargs,
        )

        self.store(prompt)
        return prompt

    def get_file_hash(self, file_path: str) -> str:
        """Get hash of a file for tracking."""
        full_path = self.repo_path / file_path

        if not full_path.exists():
            return ""

        content = full_path.read_bytes()
        return hashlib.sha256(content).hexdigest()


class ConversationLogger:
    """Log full conversations with AI assistants."""

    def __init__(self, repo_path: Optional[str] = None):
        """Initialize conversation logger."""
        if repo_path is None:
            repo_path = "."

        self.repo_path = Path(repo_path)
        self.conversations_dir = self.repo_path / ".ai-prov" / "conversations"
        self.conversations_dir.mkdir(parents=True, exist_ok=True)

    def create(self, title: Optional[str] = None, **kwargs) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(title=title, **kwargs)
        self._save(conversation)
        return conversation

    def get(self, conversation_id: str) -> Optional[Conversation]:
        """Retrieve a conversation by ID."""
        conv_file = self.conversations_dir / f"{conversation_id}.json"

        if not conv_file.exists():
            return None

        data = json.loads(conv_file.read_text())
        return Conversation(**data)

    def add_message(
        self, conversation_id: str, role: MessageRole, content: str, **kwargs
    ) -> Optional[Conversation]:
        """Add a message to a conversation."""
        conversation = self.get(conversation_id)

        if not conversation:
            return None

        message = ConversationMessage(role=role, content=content, **kwargs)
        conversation.messages.append(message)

        self._save(conversation)
        return conversation

    def end_conversation(
        self, conversation_id: str, files_created: Optional[List[str]] = None, **kwargs
    ) -> Optional[Conversation]:
        """Mark a conversation as ended."""
        conversation = self.get(conversation_id)

        if not conversation:
            return None

        conversation.ended_at = datetime.utcnow()

        if files_created:
            conversation.files_created.extend(files_created)

        for key, value in kwargs.items():
            if hasattr(conversation, key):
                setattr(conversation, key, value)

        self._save(conversation)
        return conversation

    def list_active(self) -> List[Conversation]:
        """List all active (not ended) conversations."""
        conversations = []

        for conv_file in self.conversations_dir.glob("*.json"):
            data = json.loads(conv_file.read_text())
            conv = Conversation(**data)

            if conv.ended_at is None:
                conversations.append(conv)

        return sorted(conversations, key=lambda c: c.started_at, reverse=True)

    def list_for_requirement(self, req_id: str) -> List[Conversation]:
        """List conversations that implemented a requirement."""
        conversations = []

        for conv_file in self.conversations_dir.glob("*.json"):
            data = json.loads(conv_file.read_text())
            conv = Conversation(**data)

            if req_id in conv.requirement_ids:
                conversations.append(conv)

        return conversations

    def _save(self, conversation: Conversation) -> None:
        """Save a conversation to disk."""
        conv_file = self.conversations_dir / f"{conversation.id}.json"
        conv_file.write_text(conversation.model_dump_json(indent=2))


class ProjectSpecGenerator:
    """Generate complete project specifications for regeneration."""

    def __init__(self, repo_path: Optional[str] = None):
        """Initialize project spec generator."""
        if repo_path is None:
            repo_path = "."

        self.repo_path = Path(repo_path)
        self.prompt_store = PromptStore(repo_path)
        self.conversation_logger = ConversationLogger(repo_path)

    def generate(self, name: str, description: str, **kwargs) -> ProjectSpec:
        """Generate a complete project specification."""
        spec = ProjectSpec(name=name, description=description, **kwargs)

        # Collect all prompts
        for prompt_file in self.prompt_store.prompts_dir.glob("*.json"):
            prompt_id = prompt_file.stem
            spec.prompts.append(prompt_id)

        # Collect all conversations
        for conv_file in self.conversation_logger.conversations_dir.glob("*.json"):
            conv_id = conv_file.stem
            spec.conversations.append(conv_id)

        # Build file structure
        spec.file_structure = self._get_file_structure()

        # Get file hashes
        for file in self.repo_path.rglob("*"):
            if file.is_file() and not self._should_ignore(file):
                rel_path = str(file.relative_to(self.repo_path))
                spec.files[rel_path] = self._hash_file(file)

        # Extract dependencies (if pyproject.toml or package.json exist)
        spec.dependencies = self._extract_dependencies()

        return spec

    def save_spec(self, spec: ProjectSpec, output_path: Optional[str] = None) -> Path:
        """Save project spec to file."""
        if output_path is None:
            output_path = f"project-spec-{spec.id}.json"

        output_file = Path(output_path)
        output_file.write_text(spec.model_dump_json(indent=2))
        return output_file

    def _get_file_structure(self) -> Dict:
        """Build directory tree."""
        structure = {}

        for item in self.repo_path.rglob("*"):
            if self._should_ignore(item):
                continue

            rel_path = item.relative_to(self.repo_path)
            parts = list(rel_path.parts)

            current = structure
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]

            if item.is_file():
                current[parts[-1]] = "file"
            else:
                if parts[-1] not in current:
                    current[parts[-1]] = {}

        return structure

    def _hash_file(self, file_path: Path) -> str:
        """Hash a file."""
        return hashlib.sha256(file_path.read_bytes()).hexdigest()

    def _should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored."""
        ignore_patterns = [
            ".git",
            "__pycache__",
            "node_modules",
            ".ai-prov",
            "*.pyc",
            ".DS_Store",
        ]

        path_str = str(path)
        for pattern in ignore_patterns:
            if pattern in path_str:
                return True

        return False

    def _extract_dependencies(self) -> Dict[str, str]:
        """Extract project dependencies."""
        deps = {}

        # Python (pyproject.toml)
        pyproject = self.repo_path / "pyproject.toml"
        if pyproject.exists():
            # Simple parsing - in production, use toml library
            content = pyproject.read_text()
            # Extract dependencies from pyproject.toml
            # This is simplified - use tomli in production
            deps["python"] = "extracted"

        return deps
