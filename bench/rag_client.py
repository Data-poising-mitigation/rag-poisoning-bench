"""HTTP client for RAG pipeline: upload and query."""

import httpx

# Upload can be slow (chunking + embedding); query is usually fast.
UPLOAD_TIMEOUT = 120.0
QUERY_TIMEOUT = 30.0


class RAGClient:
    """Client for RAG pipeline upload and query endpoints."""

    def __init__(self, base_url: str) -> None:
        """
        Hold base URL for pipeline (no trailing slash).
        Args:
            base_url: Base URL of the RAG pipeline service (e.g. http://localhost:8080).
        """
        self._base = base_url.rstrip("/")

    def upload_document(
        self,
        raw_content: str,
        title: str | None = None,
        metadata: dict | None = None,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
    ) -> str:
        """
        POST /upload with document content; return document_id from response.
        Args:
            raw_content: Full text of the document.
            title: Optional title.
            metadata: Optional metadata dict (default {}).
            chunk_size: Optional chunk size for pipeline.
            chunk_overlap: Optional chunk overlap for pipeline.
        Returns:
            document_id string from the pipeline response.
        Raises:
            httpx.HTTPStatusError: On non-2xx response.
        """
        payload: dict = {
            "source_type": "manual",
            "raw_content": raw_content,
            "metadata": metadata or {},
        }
        if title is not None:
            payload["title"] = title
        if chunk_size is not None:
            payload["chunk_size"] = chunk_size
        if chunk_overlap is not None:
            payload["chunk_overlap"] = chunk_overlap
        url = f"{self._base}/upload"
        print(f"[rag_client] POST {url} (title={title}) ...")
        with httpx.Client(timeout=UPLOAD_TIMEOUT) as client:
            r = client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()
            doc_id = data["document_id"]
        print(f"[rag_client] POST {url} -> document_id={doc_id}")
        return doc_id

    def query_documents(
        self,
        query: str,
        document_ids: list[str] | None,
        top_k: int = 5,
    ) -> list[dict]:
        """
        POST /query with query text and optional document_ids; return results list.
        Args:
            query: Query text.
            document_ids: Optional list of UUID strings to restrict retrieval.
            top_k: Number of results to return (default 5).
        Returns:
            List of result dicts (document_id, chunk_id, text, score).
        Raises:
            httpx.HTTPStatusError: On non-2xx response.
        """
        payload: dict = {"query": query, "top_k": top_k}
        if document_ids is not None:
            payload["document_ids"] = document_ids
        url = f"{self._base}/query"
        print(f"[rag_client] POST {url} ...")
        with httpx.Client(timeout=QUERY_TIMEOUT) as client:
            r = client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()
            results = data.get("results", [])
        print(f"[rag_client] POST {url} -> {len(results)} results")
        return results
