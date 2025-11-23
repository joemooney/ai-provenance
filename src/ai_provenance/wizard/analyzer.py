"""
Project analyzer and initialization wizard.

Uses AI agents to analyze existing projects and bootstrap AI provenance tracking.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from ai_provenance.wizard.prompts import CANNED_PROMPTS, ALL_PROMPTS, PromptTemplate


class ProjectAnalyzer:
    """Analyze existing projects using AI agents."""

    def __init__(self, repo_path: Optional[str] = None):
        """Initialize analyzer."""
        if repo_path is None:
            repo_path = "."

        self.repo_path = Path(repo_path)
        self.analysis_dir = self.repo_path / ".ai-prov" / "analysis"
        self.analysis_dir.mkdir(parents=True, exist_ok=True)

    def get_prompt_set(self, set_name: str = "standard") -> List[PromptTemplate]:
        """Get a predefined set of prompts."""
        if set_name not in CANNED_PROMPTS:
            raise ValueError(f"Unknown prompt set: {set_name}. Available: {list(CANNED_PROMPTS.keys())}")

        return CANNED_PROMPTS[set_name]

    def get_prompt(self, prompt_id: str) -> Optional[PromptTemplate]:
        """Get a specific prompt by ID."""
        for prompt in ALL_PROMPTS:
            if prompt.id == prompt_id:
                return prompt
        return None

    def save_prompt_response(self, prompt_id: str, response: Any) -> Path:
        """Save AI response to a prompt."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        response_file = self.analysis_dir / f"{prompt_id}_{timestamp}.json"

        data = {
            "prompt_id": prompt_id,
            "timestamp": timestamp,
            "response": response if isinstance(response, dict) else {"raw": str(response)},
        }

        response_file.write_text(json.dumps(data, indent=2))
        return response_file

    def load_analysis(self, prompt_id: str) -> Optional[Dict]:
        """Load the most recent analysis for a prompt."""
        # Find most recent file for this prompt
        files = sorted(self.analysis_dir.glob(f"{prompt_id}_*.json"), reverse=True)

        if not files:
            return None

        data = json.loads(files[0].read_text())
        return data.get("response")

    def has_analysis(self, prompt_id: str) -> bool:
        """Check if analysis exists for a prompt."""
        return bool(list(self.analysis_dir.glob(f"{prompt_id}_*.json")))

    def generate_initialization_plan(self) -> Dict[str, Any]:
        """Generate an initialization plan based on analysis."""
        plan = {
            "timestamp": datetime.utcnow().isoformat(),
            "steps": [],
            "recommendations": [],
        }

        # Check what analyses exist
        project_overview = self.load_analysis("project_overview")
        features = self.load_analysis("extract_features")
        requirements = self.load_analysis("extract_requirements")
        tests = self.load_analysis("analyze_tests")

        # Generate steps based on available analysis
        if project_overview:
            plan["project_info"] = project_overview

        if features:
            plan["steps"].append({
                "action": "create_features",
                "description": "Create requirement entries for extracted features",
                "count": len(features) if isinstance(features, list) else 0,
            })

        if requirements:
            plan["steps"].append({
                "action": "create_requirements",
                "description": "Create formal requirements from analysis",
                "count": len(requirements) if isinstance(requirements, list) else 0,
            })

        if tests:
            plan["steps"].append({
                "action": "map_tests",
                "description": "Map existing tests to features",
                "count": len(tests.get("tests", [])) if isinstance(tests, dict) else 0,
            })

        # Add recommendations
        if not self.has_analysis("analyze_tests"):
            plan["recommendations"].append("Run test coverage analysis to identify gaps")

        if not self.has_analysis("detect_ai_code"):
            plan["recommendations"].append("Detect and tag existing AI-generated code")

        return plan


class InitializationWizard:
    """Interactive wizard for initializing AI provenance in existing projects."""

    def __init__(self, repo_path: Optional[str] = None):
        """Initialize wizard."""
        if repo_path is None:
            repo_path = "."

        self.repo_path = Path(repo_path)
        self.analyzer = ProjectAnalyzer(repo_path)

    def run_interactive(self) -> Dict[str, Any]:
        """Run interactive initialization wizard."""
        print("\n🤖 AI Provenance Initialization Wizard\n")
        print("This wizard will analyze your project and set up AI provenance tracking.\n")

        results = {"prompts_run": [], "analyses": {}, "actions_taken": []}

        # Step 1: Choose prompt set
        print("Available prompt sets:")
        print("  1. quick          - Basic project analysis (2 prompts)")
        print("  2. standard       - Standard analysis (4 prompts)")
        print("  3. comprehensive  - Full analysis (8 prompts)")
        print("  4. with_generation - Analysis + generate docs (7 prompts)")

        # For non-interactive (Task agent), default to standard
        prompt_set_name = "standard"

        prompts = self.analyzer.get_prompt_set(prompt_set_name)

        print(f"\nWill run {len(prompts)} analysis prompts:")
        for p in prompts:
            print(f"  • {p.name}: {p.description}")

        print("\nThese prompts will be provided to an AI agent for analysis.")
        print("You can run them manually or integrate with Claude Code.\n")

        results["prompt_set"] = prompt_set_name
        results["prompts_to_run"] = [
            {"id": p.id, "name": p.name, "prompt": p.prompt} for p in prompts
        ]

        return results

    def export_prompts(self, output_file: str = "init_prompts.json") -> Path:
        """Export all prompts to a file for AI agent consumption."""
        output_path = self.repo_path / output_file

        prompts_data = {
            "project_path": str(self.repo_path),
            "generated_at": datetime.utcnow().isoformat(),
            "prompt_sets": {},
        }

        for set_name, prompts in CANNED_PROMPTS.items():
            prompts_data["prompt_sets"][set_name] = [
                {
                    "id": p.id,
                    "name": p.name,
                    "description": p.description,
                    "prompt": p.prompt,
                    "depends_on": p.depends_on,
                    "category": p.category,
                }
                for p in prompts
            ]

        output_path.write_text(json.dumps(prompts_data, indent=2))
        return output_path

    def apply_analysis_results(self, results: Dict[str, Any]) -> List[str]:
        """
        Apply analysis results to initialize the project.

        NOTE: This feature is currently disabled pending requirements-manager integration.
        Use requirements-manager CLI to create requirements from analysis results.
        """
        # TODO: Update to use requirements-manager CLI instead of old RequirementManager
        # See docs/REQUIREMENTS_MANAGER_INTEGRATION.md for details

        actions = []

        # Placeholder: Would create requirements using requirements-manager
        # For now, just save analysis results for manual processing
        if "features" in results:
            actions.append(f"Found {len(results['features'])} features - use requirements-manager to create them")

        # Create requirements from features (DISABLED - old code)
        # if "features" in results:
        #     for feature in results["features"]:
        #         req = manager.create_requirement(
        #             req_id=feature.get("id", f"FEAT-{len(actions):03d}"),
        #             title=feature.get("name", "Untitled Feature"),
        #             description=feature.get("description", ""),
        #             req_type=RequirementType.FEATURE,
        #             priority=RequirementPriority.MEDIUM,
        #         )

                # Link files (DISABLED - old code)
                for file in feature.get("files", []):
                    manager.link_file(req.id, file)

                actions.append(f"Created requirement {req.id}: {req.title}")

        # Create requirements from analysis
        if "requirements" in results:
            for req_data in results["requirements"]:
                req = manager.create_requirement(
                    req_id=req_data.get("id", f"REQ-{len(actions):03d}"),
                    title=req_data.get("title", "Untitled Requirement"),
                    description=req_data.get("description", ""),
                    req_type=RequirementType(req_data.get("type", "feature")),
                    priority=RequirementPriority(req_data.get("priority", "medium")),
                )

                actions.append(f"Created requirement {req.id}: {req.title}")

        # Map tests
        if "tests" in results and "tests" in results["tests"]:
            for test in results["tests"]["tests"]:
                test_id = test.get("id")
                for feature_id in test.get("covers", []):
                    manager.link_test(feature_id, test_id)
                    actions.append(f"Linked test {test_id} to {feature_id}")

        return actions
