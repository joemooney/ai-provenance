"""
Requirements management system.
"""

import json
from pathlib import Path
from typing import List, Optional, Dict

from ai_provenance.requirements.models import (
    Requirement,
    RequirementStatus,
    RequirementType,
    TestCase,
    TraceLink,
)


class RequirementManager:
    """Manage requirements and traceability."""

    def __init__(self, repo_path: Optional[str] = None):
        """Initialize requirements manager."""
        if repo_path is None:
            repo_path = "."

        self.repo_path = Path(repo_path)
        self.requirements_dir = self.repo_path / ".ai-prov" / "requirements"
        self.tests_dir = self.repo_path / ".ai-prov" / "tests"
        self.traces_dir = self.repo_path / ".ai-prov" / "traces"

        # Create directories
        self.requirements_dir.mkdir(parents=True, exist_ok=True)
        self.tests_dir.mkdir(parents=True, exist_ok=True)
        self.traces_dir.mkdir(parents=True, exist_ok=True)

    def create_requirement(
        self,
        req_id: str,
        title: str,
        description: str,
        req_type: RequirementType = RequirementType.FEATURE,
        **kwargs,
    ) -> Requirement:
        """Create a new requirement."""
        requirement = Requirement(
            id=req_id, title=title, description=description, type=req_type, **kwargs
        )

        self._save_requirement(requirement)
        return requirement

    def get_requirement(self, req_id: str) -> Optional[Requirement]:
        """Get a requirement by ID."""
        req_file = self.requirements_dir / f"{req_id}.json"

        if not req_file.exists():
            return None

        data = json.loads(req_file.read_text())
        return Requirement(**data)

    def update_requirement(self, req_id: str, **updates) -> Optional[Requirement]:
        """Update a requirement."""
        requirement = self.get_requirement(req_id)

        if not requirement:
            return None

        # Update fields
        for key, value in updates.items():
            if hasattr(requirement, key):
                setattr(requirement, key, value)

        # Update timestamp
        from datetime import datetime

        requirement.updated_at = datetime.utcnow()

        self._save_requirement(requirement)
        return requirement

    def list_requirements(
        self,
        status: Optional[RequirementStatus] = None,
        req_type: Optional[RequirementType] = None,
    ) -> List[Requirement]:
        """List all requirements, optionally filtered."""
        requirements = []

        for req_file in self.requirements_dir.glob("*.json"):
            data = json.loads(req_file.read_text())
            req = Requirement(**data)

            # Apply filters
            if status and req.status != status:
                continue
            if req_type and req.type != req_type:
                continue

            requirements.append(req)

        # Sort by ID
        return sorted(requirements, key=lambda r: r.id)

    def link_file(self, req_id: str, file_path: str) -> bool:
        """Link a file to a requirement."""
        requirement = self.get_requirement(req_id)

        if not requirement:
            return False

        if file_path not in requirement.files:
            requirement.files.append(file_path)
            self._save_requirement(requirement)

            # Create trace link
            self._create_trace_link("requirement", req_id, "file", file_path, "implements")

        return True

    def link_commit(self, req_id: str, commit_sha: str) -> bool:
        """Link a commit to a requirement."""
        requirement = self.get_requirement(req_id)

        if not requirement:
            return False

        if commit_sha not in requirement.commits:
            requirement.commits.append(commit_sha)
            self._save_requirement(requirement)

            # Create trace link
            self._create_trace_link("requirement", req_id, "commit", commit_sha, "implements")

        return True

    def link_test(self, req_id: str, test_id: str) -> bool:
        """Link a test case to a requirement."""
        requirement = self.get_requirement(req_id)

        if not requirement:
            return False

        if test_id not in requirement.tests:
            requirement.tests.append(test_id)
            self._save_requirement(requirement)

            # Create trace link
            self._create_trace_link("requirement", req_id, "test", test_id, "tests")

        return True

    def create_test_case(
        self, test_id: str, title: str, description: str, requirement_ids: List[str], **kwargs
    ) -> TestCase:
        """Create a test case."""
        test_case = TestCase(
            id=test_id, title=title, description=description, requirement_ids=requirement_ids, **kwargs
        )

        # Save test case
        test_file = self.tests_dir / f"{test_id}.json"
        test_file.write_text(test_case.model_dump_json(indent=2))

        # Link to requirements
        for req_id in requirement_ids:
            self.link_test(req_id, test_id)

        return test_case

    def get_test_case(self, test_id: str) -> Optional[TestCase]:
        """Get a test case by ID."""
        test_file = self.tests_dir / f"{test_id}.json"

        if not test_file.exists():
            return None

        data = json.loads(test_file.read_text())
        return TestCase(**data)

    def get_coverage(self, req_id: str) -> Dict[str, any]:
        """Get test coverage for a requirement."""
        requirement = self.get_requirement(req_id)

        if not requirement:
            return {}

        return {
            "requirement_id": req_id,
            "files": len(requirement.files),
            "commits": len(requirement.commits),
            "tests": len(requirement.tests),
            "status": requirement.status.value,
            "covered": len(requirement.tests) > 0,
        }

    def get_traceability_matrix(self) -> Dict[str, Dict]:
        """Generate full traceability matrix."""
        requirements = self.list_requirements()
        matrix = {}

        for req in requirements:
            matrix[req.id] = {
                "title": req.title,
                "status": req.status.value,
                "type": req.type.value,
                "files": req.files,
                "commits": req.commits,
                "tests": req.tests,
                "ai_generated": req.ai_generated,
                "coverage": self.get_coverage(req.id),
            }

        return matrix

    def _save_requirement(self, requirement: Requirement) -> None:
        """Save a requirement to disk."""
        req_file = self.requirements_dir / f"{requirement.id}.json"
        req_file.write_text(requirement.model_dump_json(indent=2))

    def _create_trace_link(
        self, source_type: str, source_id: str, target_type: str, target_id: str, link_type: str
    ) -> None:
        """Create a bidirectional trace link."""
        link = TraceLink(
            source_type=source_type,
            source_id=source_id,
            target_type=target_type,
            target_id=target_id,
            link_type=link_type,
        )

        # Save link
        link_file = self.traces_dir / f"{source_type}_{source_id}_{target_type}_{target_id}.json"
        link_file.write_text(link.model_dump_json(indent=2))

    def find_by_file(self, file_path: str) -> List[Requirement]:
        """Find all requirements linked to a file."""
        requirements = []

        for req in self.list_requirements():
            if file_path in req.files:
                requirements.append(req)

        return requirements

    def find_untested(self) -> List[Requirement]:
        """Find requirements without test coverage."""
        return [req for req in self.list_requirements() if len(req.tests) == 0]

    def find_by_status(self, status: RequirementStatus) -> List[Requirement]:
        """Find requirements by status."""
        return self.list_requirements(status=status)
