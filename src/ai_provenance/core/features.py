"""
Feature flag system for AI Provenance.

Allows enabling/disabling features during initialization and runtime.
"""

from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set
import json

from pydantic import BaseModel, Field


class Feature(str, Enum):
    """Available features in AI Provenance."""

    # Core features (always enabled)
    CORE_TRACKING = "core_tracking"  # Basic metadata tracking
    GIT_NOTES = "git_notes"  # Git notes integration
    INLINE_METADATA = "inline_metadata"  # Inline comment metadata

    # Optional features
    REQUIREMENTS = "requirements"  # Requirements management
    TEST_TRACEABILITY = "test_traceability"  # Test case tracking
    PROMPTS = "prompts"  # Prompt storage
    CONVERSATIONS = "conversations"  # Full conversation logging
    AUTO_DETECTION = "auto_detection"  # Automatic AI code detection
    FILE_METADATA = "file_metadata"  # .meta.json generation
    WEB_DASHBOARD = "web_dashboard"  # Web UI
    IDE_INTEGRATION = "ide_integration"  # IDE extensions
    CI_VALIDATION = "ci_validation"  # CI/CD validation
    TEAM_FEATURES = "team_features"  # Multi-user collaboration
    AUDIT_TRAIL = "audit_trail"  # Enhanced audit features
    REGENERATION = "regeneration"  # Project regeneration
    API_SERVER = "api_server"  # REST API server
    METRICS = "metrics"  # Advanced metrics and analytics


class FeatureStatus(str, Enum):
    """Status of a feature."""

    ENABLED = "enabled"
    DISABLED = "disabled"
    ALPHA = "alpha"  # Experimental, may break
    BETA = "beta"  # Mostly stable, but testing
    STABLE = "stable"  # Production-ready
    DEPRECATED = "deprecated"  # Will be removed


class FeatureConfig(BaseModel):
    """Configuration for a single feature."""

    name: Feature
    enabled: bool = False
    status: FeatureStatus = FeatureStatus.STABLE
    description: str
    dependencies: List[Feature] = Field(default_factory=list)
    config: Dict[str, any] = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "requirements",
                "enabled": True,
                "status": "stable",
                "description": "Requirements management and traceability",
                "dependencies": ["core_tracking"],
                "config": {"storage": "json", "auto_link": True},
            }
        }


class FeatureSet(BaseModel):
    """Complete feature configuration for a repository."""

    features: Dict[Feature, FeatureConfig] = Field(default_factory=dict)
    profiles: Dict[str, List[Feature]] = Field(default_factory=dict)

    def is_enabled(self, feature: Feature) -> bool:
        """Check if a feature is enabled."""
        if feature not in self.features:
            return False
        return self.features[feature].enabled

    def enable(self, feature: Feature) -> None:
        """Enable a feature and its dependencies."""
        if feature not in self.features:
            raise ValueError(f"Unknown feature: {feature}")

        config = self.features[feature]

        # Enable dependencies first
        for dep in config.dependencies:
            if not self.is_enabled(dep):
                self.enable(dep)

        config.enabled = True

    def disable(self, feature: Feature) -> None:
        """Disable a feature and features that depend on it."""
        if feature not in self.features:
            raise ValueError(f"Unknown feature: {feature}")

        # Find and disable dependent features
        for other_feature, other_config in self.features.items():
            if feature in other_config.dependencies and other_config.enabled:
                self.disable(other_feature)

        self.features[feature].enabled = False

    def get_enabled_features(self) -> Set[Feature]:
        """Get all enabled features."""
        return {f for f, config in self.features.items() if config.enabled}

    def apply_profile(self, profile_name: str) -> None:
        """Apply a feature profile."""
        if profile_name not in self.profiles:
            raise ValueError(f"Unknown profile: {profile_name}")

        # Disable all optional features first
        for feature in self.features:
            if feature not in [Feature.CORE_TRACKING, Feature.GIT_NOTES, Feature.INLINE_METADATA]:
                self.disable(feature)

        # Enable profile features
        for feature in self.profiles[profile_name]:
            self.enable(feature)


# Default feature definitions
DEFAULT_FEATURES: Dict[Feature, FeatureConfig] = {
    # Core (always enabled)
    Feature.CORE_TRACKING: FeatureConfig(
        name=Feature.CORE_TRACKING,
        enabled=True,
        status=FeatureStatus.STABLE,
        description="Core metadata tracking functionality",
        dependencies=[],
    ),
    Feature.GIT_NOTES: FeatureConfig(
        name=Feature.GIT_NOTES,
        enabled=True,
        status=FeatureStatus.STABLE,
        description="Git notes integration for immutable metadata",
        dependencies=[Feature.CORE_TRACKING],
    ),
    Feature.INLINE_METADATA: FeatureConfig(
        name=Feature.INLINE_METADATA,
        enabled=True,
        status=FeatureStatus.STABLE,
        description="Inline comment-based metadata",
        dependencies=[Feature.CORE_TRACKING],
    ),
    # Optional features
    Feature.REQUIREMENTS: FeatureConfig(
        name=Feature.REQUIREMENTS,
        enabled=False,
        status=FeatureStatus.BETA,
        description="Requirements management and traceability",
        dependencies=[Feature.CORE_TRACKING],
        config={"storage": "json", "auto_link": True},
    ),
    Feature.TEST_TRACEABILITY: FeatureConfig(
        name=Feature.TEST_TRACEABILITY,
        enabled=False,
        status=FeatureStatus.BETA,
        description="Test case tracking and coverage",
        dependencies=[Feature.CORE_TRACKING],
    ),
    Feature.PROMPTS: FeatureConfig(
        name=Feature.PROMPTS,
        enabled=False,
        status=FeatureStatus.ALPHA,
        description="Store prompts used to generate code",
        dependencies=[Feature.CORE_TRACKING],
        config={"storage": ".ai-prov/prompts", "encrypt": False},
    ),
    Feature.CONVERSATIONS: FeatureConfig(
        name=Feature.CONVERSATIONS,
        enabled=False,
        status=FeatureStatus.ALPHA,
        description="Log full AI conversations",
        dependencies=[Feature.PROMPTS],
        config={"storage": ".ai-prov/conversations", "format": "json"},
    ),
    Feature.AUTO_DETECTION: FeatureConfig(
        name=Feature.AUTO_DETECTION,
        enabled=False,
        status=FeatureStatus.ALPHA,
        description="Automatically detect AI-generated code",
        dependencies=[Feature.CORE_TRACKING],
        config={"confidence_threshold": 0.7},
    ),
    Feature.FILE_METADATA: FeatureConfig(
        name=Feature.FILE_METADATA,
        enabled=False,
        status=FeatureStatus.ALPHA,
        description="Generate .meta.json files automatically",
        dependencies=[Feature.CORE_TRACKING],
    ),
    Feature.WEB_DASHBOARD: FeatureConfig(
        name=Feature.WEB_DASHBOARD,
        enabled=False,
        status=FeatureStatus.ALPHA,
        description="Web-based dashboard for visualization",
        dependencies=[Feature.CORE_TRACKING, Feature.METRICS],
        config={"port": 5100, "host": "localhost"},
    ),
    Feature.IDE_INTEGRATION: FeatureConfig(
        name=Feature.IDE_INTEGRATION,
        enabled=False,
        status=FeatureStatus.ALPHA,
        description="IDE extensions and integrations",
        dependencies=[Feature.CORE_TRACKING],
    ),
    Feature.CI_VALIDATION: FeatureConfig(
        name=Feature.CI_VALIDATION,
        enabled=True,
        status=FeatureStatus.STABLE,
        description="CI/CD validation and gates",
        dependencies=[Feature.CORE_TRACKING],
    ),
    Feature.TEAM_FEATURES: FeatureConfig(
        name=Feature.TEAM_FEATURES,
        enabled=False,
        status=FeatureStatus.ALPHA,
        description="Multi-user collaboration features",
        dependencies=[Feature.CORE_TRACKING],
    ),
    Feature.AUDIT_TRAIL: FeatureConfig(
        name=Feature.AUDIT_TRAIL,
        enabled=False,
        status=FeatureStatus.BETA,
        description="Enhanced audit and compliance features",
        dependencies=[Feature.CORE_TRACKING, Feature.GIT_NOTES],
    ),
    Feature.REGENERATION: FeatureConfig(
        name=Feature.REGENERATION,
        enabled=False,
        status=FeatureStatus.ALPHA,
        description="Project regeneration from metadata",
        dependencies=[Feature.PROMPTS, Feature.CONVERSATIONS, Feature.REQUIREMENTS],
    ),
    Feature.API_SERVER: FeatureConfig(
        name=Feature.API_SERVER,
        enabled=False,
        status=FeatureStatus.ALPHA,
        description="REST API server for integrations",
        dependencies=[Feature.CORE_TRACKING],
        config={"port": 5101, "host": "localhost"},
    ),
    Feature.METRICS: FeatureConfig(
        name=Feature.METRICS,
        enabled=True,
        status=FeatureStatus.STABLE,
        description="Advanced metrics and analytics",
        dependencies=[Feature.CORE_TRACKING],
    ),
}

# Feature profiles for common use cases
DEFAULT_PROFILES: Dict[str, List[Feature]] = {
    "minimal": [
        Feature.CORE_TRACKING,
        Feature.GIT_NOTES,
        Feature.INLINE_METADATA,
    ],
    "standard": [
        Feature.CORE_TRACKING,
        Feature.GIT_NOTES,
        Feature.INLINE_METADATA,
        Feature.REQUIREMENTS,
        Feature.TEST_TRACEABILITY,
        Feature.CI_VALIDATION,
        Feature.METRICS,
    ],
    "full": [
        Feature.CORE_TRACKING,
        Feature.GIT_NOTES,
        Feature.INLINE_METADATA,
        Feature.REQUIREMENTS,
        Feature.TEST_TRACEABILITY,
        Feature.PROMPTS,
        Feature.CONVERSATIONS,
        Feature.AUTO_DETECTION,
        Feature.CI_VALIDATION,
        Feature.METRICS,
        Feature.AUDIT_TRAIL,
    ],
    "team": [
        Feature.CORE_TRACKING,
        Feature.GIT_NOTES,
        Feature.INLINE_METADATA,
        Feature.REQUIREMENTS,
        Feature.TEST_TRACEABILITY,
        Feature.CI_VALIDATION,
        Feature.TEAM_FEATURES,
        Feature.WEB_DASHBOARD,
        Feature.METRICS,
        Feature.AUDIT_TRAIL,
    ],
    "research": [
        Feature.CORE_TRACKING,
        Feature.GIT_NOTES,
        Feature.INLINE_METADATA,
        Feature.PROMPTS,
        Feature.CONVERSATIONS,
        Feature.METRICS,
        Feature.AUTO_DETECTION,
    ],
    "regeneration": [
        Feature.CORE_TRACKING,
        Feature.GIT_NOTES,
        Feature.INLINE_METADATA,
        Feature.REQUIREMENTS,
        Feature.TEST_TRACEABILITY,
        Feature.PROMPTS,
        Feature.CONVERSATIONS,
        Feature.REGENERATION,
    ],
}


def create_default_feature_set() -> FeatureSet:
    """Create a feature set with default configuration."""
    return FeatureSet(features=DEFAULT_FEATURES.copy(), profiles=DEFAULT_PROFILES.copy())


def load_feature_config(repo_path: Optional[str] = None) -> FeatureSet:
    """
    Load feature configuration from repository.

    Args:
        repo_path: Path to repository (default: current directory)

    Returns:
        FeatureSet configuration
    """
    if repo_path is None:
        repo_path = "."

    config_path = Path(repo_path) / ".ai-prov" / "features.json"

    if config_path.exists():
        data = json.loads(config_path.read_text())
        return FeatureSet(**data)
    else:
        return create_default_feature_set()


def save_feature_config(feature_set: FeatureSet, repo_path: Optional[str] = None) -> None:
    """
    Save feature configuration to repository.

    Args:
        feature_set: FeatureSet to save
        repo_path: Path to repository (default: current directory)
    """
    if repo_path is None:
        repo_path = "."

    config_dir = Path(repo_path) / ".ai-prov"
    config_dir.mkdir(exist_ok=True)

    config_path = config_dir / "features.json"
    config_path.write_text(feature_set.model_dump_json(indent=2))
