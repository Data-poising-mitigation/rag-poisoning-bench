"""Read and write state/corpus_used.json."""

import json
from pathlib import Path


def read_state(path: Path) -> dict | None:
    """
    Load state from a JSON file; return None if file is missing or invalid.
    Args:
        path: Path to corpus_used.json.
    Returns:
        State dict (hasUploaded, documents, optional seeded_at) or None.
    """
    if not path.exists():
        return None
    try:
        data = path.read_text(encoding="utf-8")
        return json.loads(data)
    except (json.JSONDecodeError, OSError):
        return None  # invalid or unreadable


def write_state(path: Path, state: dict) -> None:
    """
    Write state dict to JSON with sensible indent.
    Args:
        path: Path to corpus_used.json (parent created if needed).
        state: Dict with hasUploaded, documents, optional seeded_at.
    Returns:
        None.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")
