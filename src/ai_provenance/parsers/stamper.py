"""
File stamping with AI provenance inline metadata.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

from ai_provenance.core.models import AITool, Confidence

# Language to comment style mapping
COMMENT_STYLES = {
    # Single-line comment languages
    ".py": "#",
    ".rb": "#",
    ".sh": "#",
    ".bash": "#",
    ".yaml": "#",
    ".yml": "#",
    ".toml": "#",
    ".r": "#",
    # C-style languages
    ".js": "//",
    ".ts": "//",
    ".jsx": "//",
    ".tsx": "//",
    ".java": "//",
    ".c": "//",
    ".cpp": "//",
    ".cc": "//",
    ".h": "//",
    ".hpp": "//",
    ".cs": "//",
    ".go": "//",
    ".rs": "//",
    ".swift": "//",
    ".kt": "//",
    ".scala": "//",
    ".php": "//",
    # Others
    ".sql": "--",
    ".lua": "--",
    ".hs": "--",
    ".ml": "(*",  # Special case: OCaml uses (* *)
    ".ex": "#",  # Elixir
    ".exs": "#",
}


def detect_comment_style(file_path: str) -> str:
    """
    Detect the comment style for a file based on extension.

    Args:
        file_path: Path to the file

    Returns:
        Comment prefix (e.g., '#', '//', '--')
    """
    ext = Path(file_path).suffix.lower()
    return COMMENT_STYLES.get(ext, "#")  # Default to #


def format_inline_metadata(
    tool: str,
    confidence: str,
    trace: Optional[List[str]] = None,
    tests: Optional[List[str]] = None,
    reviewer: Optional[str] = None,
    comment_style: str = "#",
) -> str:
    """
    Format inline metadata comment.

    Args:
        tool: AI tool name
        confidence: Confidence level (high, med, low)
        trace: Requirement IDs
        tests: Test case IDs
        reviewer: Reviewer name/email
        comment_style: Comment prefix

    Returns:
        Formatted inline comment

    Example:
        # ai:claude:high | trace:SPEC-89 | test:TC-210 | reviewed:2025-11-16:alice
    """
    parts = [f"ai:{tool}:{confidence}"]

    if trace:
        parts.append(f"trace:{','.join(trace)}")

    if tests:
        parts.append(f"test:{','.join(tests)}")

    if reviewer:
        date = datetime.utcnow().strftime("%Y-%m-%d")
        reviewer_name = reviewer.split("@")[0] if "@" in reviewer else reviewer
        parts.append(f"reviewed:{date}:{reviewer_name}")

    metadata = " | ".join(parts)

    # Handle multi-line comment styles
    if comment_style == "(*":
        return f"(* {metadata} *)"
    elif comment_style == "/*":
        return f"/* {metadata} */"
    else:
        return f"{comment_style} {metadata}"


def stamp_file(
    file_path: str,
    tool: str,
    confidence: str,
    trace: Optional[List[str]] = None,
    tests: Optional[List[str]] = None,
    reviewer: Optional[str] = None,
    position: str = "top",
) -> None:
    """
    Add AI provenance metadata to a file.

    Args:
        file_path: Path to the file
        tool: AI tool used
        confidence: Confidence level (high, med, low)
        trace: Requirement IDs
        tests: Test case IDs
        reviewer: Reviewer email
        position: Where to add metadata ('top', 'bottom')

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If invalid parameters
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Validate tool and confidence
    try:
        AITool(tool)
    except ValueError:
        raise ValueError(f"Invalid AI tool: {tool}")

    try:
        Confidence(confidence)
    except ValueError:
        raise ValueError(f"Invalid confidence: {confidence}")

    # Detect comment style
    comment_style = detect_comment_style(file_path)

    # Create metadata comment
    metadata_line = format_inline_metadata(
        tool=tool,
        confidence=confidence,
        trace=trace,
        tests=tests,
        reviewer=reviewer,
        comment_style=comment_style,
    )

    # Read file
    content = path.read_text()

    # Check if metadata already exists
    if re.search(r"ai:" + re.escape(tool), content):
        # Update existing metadata
        pattern = r"^[#/\-*]+\s*ai:.*$"
        if re.search(pattern, content, re.MULTILINE):
            content = re.sub(pattern, metadata_line, content, count=1, flags=re.MULTILINE)
    else:
        # Add new metadata
        if position == "top":
            # Add after shebang or at the very top
            lines = content.split("\n")
            insert_pos = 0

            # Skip shebang
            if lines and lines[0].startswith("#!"):
                insert_pos = 1

            # Skip encoding declarations
            if insert_pos < len(lines) and (
                "coding:" in lines[insert_pos] or "encoding:" in lines[insert_pos]
            ):
                insert_pos += 1

            lines.insert(insert_pos, metadata_line)
            content = "\n".join(lines)
        else:  # bottom
            content = content.rstrip() + "\n\n" + metadata_line + "\n"

    # Write back
    path.write_text(content)


def parse_inline_metadata(file_path: str) -> List[Tuple[int, dict]]:
    """
    Parse all inline AI metadata from a file.

    Args:
        file_path: Path to the file

    Returns:
        List of (line_number, metadata_dict) tuples

    Example metadata_dict:
        {
            'tool': 'claude',
            'confidence': 'high',
            'trace': 'SPEC-89',
            'tests': ['TC-210'],
            'reviewed': '2025-11-16:alice'
        }
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    results = []
    content = path.read_text()

    # Pattern to match ai: metadata
    pattern = r"^\s*[#/\-*]+\s*(ai:.+)$"

    for line_num, line in enumerate(content.split("\n"), 1):
        match = re.search(pattern, line)
        if match:
            metadata_str = match.group(1)
            metadata = _parse_metadata_string(metadata_str)
            if metadata:
                results.append((line_num, metadata))

    return results


def _parse_metadata_string(metadata_str: str) -> Optional[dict]:
    """
    Parse metadata string into dict.

    Args:
        metadata_str: e.g., "ai:claude:high | trace:SPEC-89 | test:TC-210"

    Returns:
        Parsed metadata dict
    """
    metadata = {}

    parts = [p.strip() for p in metadata_str.split("|")]

    for part in parts:
        if part.startswith("ai:"):
            # Parse ai:tool:conf
            ai_parts = part.split(":")
            if len(ai_parts) >= 2:
                metadata["tool"] = ai_parts[1]
            if len(ai_parts) >= 3:
                metadata["confidence"] = ai_parts[2]

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

    return metadata if metadata else None


def find_ai_hunks(file_path: str) -> List[Tuple[int, int, dict]]:
    """
    Find all AI-generated code hunks in a file.

    A hunk is defined as a continuous block of code following an AI metadata comment.

    Args:
        file_path: Path to the file

    Returns:
        List of (start_line, end_line, metadata) tuples
    """
    metadata_lines = parse_inline_metadata(file_path)
    if not metadata_lines:
        return []

    hunks = []
    path = Path(file_path)
    lines = path.read_text().split("\n")

    for line_num, metadata in metadata_lines:
        # Find the extent of the hunk
        start = line_num
        end = _find_hunk_end(lines, line_num)
        hunks.append((start, end, metadata))

    return hunks


def _find_hunk_end(lines: List[str], start: int) -> int:
    """
    Find the end of a code hunk starting at start line.

    Uses heuristics:
    - Stop at next metadata comment
    - Stop at blank line followed by another metadata comment
    - Stop at significant indentation change
    """
    # Simple heuristic: next metadata comment or end of file
    for i in range(start, len(lines)):
        if re.search(r"^\s*[#/\-*]+\s*ai:", lines[i]):
            return i - 1

    return len(lines)
