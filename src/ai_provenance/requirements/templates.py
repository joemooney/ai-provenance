"""
Requirement templates and format conversion.
"""

import re
import json
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from datetime import datetime

import yaml

from ai_provenance.requirements.models import (
    Requirement,
    RequirementType,
    RequirementStatus,
    RequirementPriority,
)


def parse_yaml_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """
    Parse YAML front-matter from Markdown content.

    Args:
        content: Markdown content with YAML front-matter

    Returns:
        Tuple of (metadata dict, body markdown)
    """
    # Match YAML front-matter (--- ... ---)
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return {}, content

    yaml_content = match.group(1)
    body = match.group(2)

    try:
        metadata = yaml.safe_load(yaml_content)
        return metadata or {}, body
    except yaml.YAMLError:
        return {}, content


def markdown_to_requirement(md_path: Path) -> Requirement:
    """
    Convert Markdown requirement (with YAML front-matter) to Requirement object.

    Args:
        md_path: Path to Markdown file

    Returns:
        Requirement object
    """
    content = md_path.read_text()
    metadata, body = parse_yaml_frontmatter(content)

    # Extract title from first heading
    title_match = re.search(r'^# .+?: (.+)$', body, re.MULTILINE)
    title = title_match.group(1) if title_match else metadata.get('title', 'Untitled')

    # Extract requirement statement (section 1)
    desc_match = re.search(r'## 1\. Requirement Statement\s*\n(.+?)(?=\n##|\Z)', body, re.DOTALL)
    description = desc_match.group(1).strip() if desc_match else ''

    # Map YAML to Requirement fields
    req = Requirement(
        id=metadata.get('id', md_path.stem),
        title=title,
        description=description,
        type=RequirementType(metadata.get('type', 'feature')),
        status=RequirementStatus(metadata.get('status', 'planned').lower().replace(' ', '-')),
        priority=RequirementPriority(metadata.get('priority', 'medium').lower()),
        created_by=metadata.get('authors', [None])[0] if metadata.get('authors') else None,
        parent=metadata.get('parent'),
        tags=metadata.get('tags', []),
        ai_generated=metadata.get('ai_generated', False),
        ai_tool=metadata.get('ai_tool'),
    )

    # Extract test cases from fit criterion table
    test_matches = re.finditer(r'\| (TC-\d+)', body)
    req.tests = [match.group(1) for match in test_matches]

    # Extract dependencies
    deps_match = re.search(r'## 5\. Dependencies\s*\n(.+?)(?=\n##|\Z)', body, re.DOTALL)
    if deps_match:
        dep_text = deps_match.group(1)
        dep_ids = re.findall(r'(SPEC-\d+)', dep_text)
        req.related = dep_ids

    return req


def requirement_to_markdown(req: Requirement, template_name: str = 'ieee830') -> str:
    """
    Convert Requirement object to Markdown with YAML front-matter.

    Args:
        req: Requirement object
        template_name: Template to use

    Returns:
        Markdown string
    """
    template_path = Path(__file__).parent / 'templates' / f'{template_name}.md'

    if not template_path.exists():
        raise ValueError(f"Template not found: {template_name}")

    template = template_path.read_text()

    # Prepare template variables
    created_at = req.created_at.strftime('%Y-%m-%d') if hasattr(req, 'created_at') and req.created_at else datetime.utcnow().strftime('%Y-%m-%d')

    vars_dict = {
        'id': req.id,
        'title': req.title,
        'description': req.description,
        'priority': req.priority.value.title() if hasattr(req.priority, 'value') else str(req.priority).title(),
        'status': req.status.value.title() if hasattr(req.status, 'value') else str(req.status).title(),
        'ai_generated': str(req.ai_generated).lower(),
        'ai_tool': req.ai_tool or 'null',
        'ai_confidence': 'null',  # Add to model if needed
        'author': req.created_by or 'unknown',
        'parent': req.parent or 'null',
        'tags': json.dumps(req.tags) if req.tags else '[]',
        'test_id': req.tests[0] if req.tests else 'TC-XXX',
        'dependencies': '\n'.join([f'- {dep}' for dep in req.related]) if req.related else '- None',
        'created_at': created_at,
    }

    # Replace template variables
    output = template
    for key, value in vars_dict.items():
        output = output.replace(f'{{{key}}}', str(value))

    return output


def sync_markdown_to_json(specs_dir: Path, json_dir: Path) -> int:
    """
    Sync Markdown requirements to JSON format.

    Args:
        specs_dir: Directory containing Markdown specs
        json_dir: Directory for JSON output

    Returns:
        Number of files synced
    """
    count = 0

    for md_file in specs_dir.glob('SPEC-*.md'):
        try:
            req = markdown_to_requirement(md_file)

            # Save as JSON
            json_file = json_dir / f'{req.id}.json'
            json_file.write_text(req.model_dump_json(indent=2))

            count += 1
        except Exception as e:
            print(f"Error processing {md_file}: {e}")

    return count


def sync_json_to_markdown(json_dir: Path, specs_dir: Path, template: str = 'ieee830') -> int:
    """
    Sync JSON requirements to Markdown format.

    Args:
        json_dir: Directory containing JSON requirements
        specs_dir: Directory for Markdown output
        template: Template name to use

    Returns:
        Number of files synced
    """
    count = 0

    for json_file in json_dir.glob('SPEC-*.json'):
        try:
            data = json.loads(json_file.read_text())
            req = Requirement(**data)

            # Convert to Markdown
            md_content = requirement_to_markdown(req, template)

            # Save
            md_file = specs_dir / f'{req.id}.md'
            md_file.write_text(md_content)

            count += 1
        except Exception as e:
            print(f"Error processing {json_file}: {e}")

    return count
