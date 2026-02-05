"""Load .env and expose pipeline URL and repo root."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def get_pipeline_base_url() -> str:
    """
    Return the RAG pipeline base URL from RAG_PIPELINE_URL, without trailing slash.
    Returns:
        Base URL string.
    Raises:
        ValueError: If RAG_PIPELINE_URL is missing or empty.
    """
    url = os.getenv("RAG_PIPELINE_URL", "").strip()
    if not url:
        raise ValueError("RAG_PIPELINE_URL is not set. Set it in .env (e.g. http://localhost:8080).")
    return url.rstrip("/")


def get_repo_root() -> Path:
    """
    Return the repo root directory (parent of run.py / bench package).
    Returns:
        Path to repo root.
    """
    return Path(__file__).resolve().parent.parent
