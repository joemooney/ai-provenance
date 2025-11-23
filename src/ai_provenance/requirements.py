"""
Lightweight requirements.yaml reader for requirements-manager integration.

This module provides simple functions to read requirements from requirements-manager's
YAML file format. It does NOT manage requirements - that's done by requirements-manager.
"""

from pathlib import Path
from typing import List, Dict, Optional
import yaml


def load_requirements(yaml_path: str = "requirements.yaml") -> List[Dict]:
    """
    Load requirements from requirements-manager YAML file.

    Args:
        yaml_path: Path to requirements.yaml file

    Returns:
        List of requirement dictionaries
    """
    path = Path(yaml_path)

    if not path.exists():
        return []

    with open(path) as f:
        data = yaml.safe_load(f)

    return data.get("requirements", [])


def load_mapping(mapping_path: str = ".requirements-mapping.yaml") -> Dict[str, str]:
    """
    Load UUID → SPEC-ID mapping from requirements-manager export.

    Args:
        mapping_path: Path to mapping file

    Returns:
        Dictionary mapping UUIDs to SPEC-IDs
    """
    path = Path(mapping_path)

    if not path.exists():
        return {}

    with open(path) as f:
        data = yaml.safe_load(f)

    return data.get("mappings", {})


def get_requirement_by_uuid(
    uuid: str, yaml_path: str = "requirements.yaml"
) -> Optional[Dict]:
    """
    Get requirement by UUID.

    Args:
        uuid: UUID of the requirement
        yaml_path: Path to requirements.yaml

    Returns:
        Requirement dictionary or None if not found
    """
    reqs = load_requirements(yaml_path)

    for req in reqs:
        if req.get("id") == uuid:
            return req

    return None


def get_requirement_by_spec_id(
    spec_id: str,
    yaml_path: str = "requirements.yaml",
    mapping_path: str = ".requirements-mapping.yaml",
) -> Optional[Dict]:
    """
    Get requirement by SPEC-ID (e.g., SPEC-001).

    Args:
        spec_id: SPEC-ID to look up
        yaml_path: Path to requirements.yaml
        mapping_path: Path to mapping file

    Returns:
        Requirement dictionary or None if not found
    """
    # Load mapping to get UUID
    mapping = load_mapping(mapping_path)

    # Reverse lookup: SPEC-ID → UUID
    uuid = None
    for u, s in mapping.items():
        if s == spec_id:
            uuid = u
            break

    if not uuid:
        return None

    # Get requirement by UUID
    return get_requirement_by_uuid(uuid, yaml_path)


def get_spec_id_for_uuid(
    uuid: str, mapping_path: str = ".requirements-mapping.yaml"
) -> Optional[str]:
    """
    Get SPEC-ID for a UUID.

    Args:
        uuid: UUID to look up
        mapping_path: Path to mapping file

    Returns:
        SPEC-ID (e.g., "SPEC-001") or None if not found
    """
    mapping = load_mapping(mapping_path)
    return mapping.get(uuid)


def get_uuid_for_spec_id(
    spec_id: str, mapping_path: str = ".requirements-mapping.yaml"
) -> Optional[str]:
    """
    Get UUID for a SPEC-ID (reverse lookup).

    Args:
        spec_id: SPEC-ID to look up
        mapping_path: Path to mapping file

    Returns:
        UUID or None if not found
    """
    mapping = load_mapping(mapping_path)

    for uuid, sid in mapping.items():
        if sid == spec_id:
            return uuid

    return None


def get_all_spec_ids(mapping_path: str = ".requirements-mapping.yaml") -> List[str]:
    """
    Get all SPEC-IDs from mapping.

    Args:
        mapping_path: Path to mapping file

    Returns:
        List of SPEC-IDs
    """
    mapping = load_mapping(mapping_path)
    return list(mapping.values())
