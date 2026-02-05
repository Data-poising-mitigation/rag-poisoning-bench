"""Load test case config, queries, and resolve corpus paths."""

import json
from pathlib import Path


def load_config(path: Path) -> dict:
    """
    Read config.json and return dict with corpus_paths, top_k, etc.
    Args:
        path: Path to test case folder (e.g. test-cases/test1).
    Returns:
        Config dict with corpus_paths, top_k, name, description, etc.
    Raises:
        FileNotFoundError: If config.json is missing.
        ValueError: If config is invalid or missing required keys.
    """
    config_path = path / "config.json"
    if not config_path.exists():
        raise FileNotFoundError(f"config.json not found: {config_path}")
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        raise ValueError(f"Invalid config.json at {config_path}: {e}") from e
    if not isinstance(data.get("corpus_paths"), list) or not data["corpus_paths"]:
        raise ValueError(f"config.json must have non-empty corpus_paths list: {config_path}")
    return data


def load_queries(path: Path) -> list[dict]:
    """
    Read queries/queries.json and return list of { id, text }.
    Args:
        path: Path to test case folder (e.g. test-cases/test1).
    Returns:
        List of dicts with id and text keys.
    Raises:
        FileNotFoundError: If queries.json is missing.
        ValueError: If structure is invalid.
    """
    queries_path = path / "queries" / "queries.json"
    if not queries_path.exists():
        raise FileNotFoundError(f"queries.json not found: {queries_path}")
    try:
        data = json.loads(queries_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        raise ValueError(f"Invalid queries.json at {queries_path}: {e}") from e
    if not isinstance(data, list):
        raise ValueError(f"queries.json must be a list: {queries_path}")
    for i, item in enumerate(data):
        if not isinstance(item, dict) or "text" not in item:
            raise ValueError(f"queries.json[{i}] must be an object with 'text': {queries_path}")
    return data


def resolve_corpus_path(repo_root: Path, corpus_path: str) -> Path:
    """
    Resolve repo-root-relative corpus path to absolute Path; raise if outside repo or missing.
    Args:
        repo_root: Repo root directory.
        corpus_path: Relative path (e.g. corpus/policy_trust_docs.txt).
    Returns:
        Absolute Path to the corpus file.
    Raises:
        ValueError: If path is outside repo_root or file is missing.
    """
    resolved = (repo_root / corpus_path).resolve()
    try:
        resolved.relative_to(repo_root.resolve())
    except ValueError:
        raise ValueError(f"Corpus path must be under repo root: {corpus_path}") from None
    if not resolved.exists() or not resolved.is_file():
        raise FileNotFoundError(f"Corpus file not found: {resolved}")
    return resolved
