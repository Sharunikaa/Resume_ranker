"""
ChromaDB client with local persistence.
Uses CHROMA_PERSIST_DIR from env.
"""

import os
from typing import List, Optional

import chromadb
from chromadb.config import Settings

_persistent_client: Optional[chromadb.PersistentClient] = None


def get_chroma_client() -> chromadb.PersistentClient:
    """Get or create persistent ChromaDB client."""
    global _persistent_client
    if _persistent_client is None:
        persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
        _persistent_client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False),
        )
    return _persistent_client


# ChromaDB rejects empty metadata; use a placeholder when no metadata is provided
_EMPTY_METADATA_PLACEHOLDER = {"_": 1}


def get_or_create_collection(name: str, metadata: Optional[dict] = None):
    """Get or create a collection by name."""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=name, metadata=metadata if metadata else _EMPTY_METADATA_PLACEHOLDER
    )


def get_job_embeddings_collection_name(job_id: str) -> str:
    """Collection name for job embedding (one per job)."""
    return f"job_emb_{job_id}"


def get_candidates_collection_name(job_id: str) -> str:
    """Collection name for candidate embeddings for a job."""
    return f"candidates_{job_id}"


def store_embedding(
    collection_name: str,
    id: str,
    embedding: List[float],
    metadata: Optional[dict] = None,
) -> None:
    """Store a single embedding in the collection."""
    coll = get_or_create_collection(collection_name)
    meta = metadata if metadata else _EMPTY_METADATA_PLACEHOLDER
    coll.upsert(
        ids=[id],
        embeddings=[embedding],
        metadatas=[meta],
    )


def get_embedding(collection_name: str, id: str) -> Optional[List[float]]:
    """Get embedding by id. Returns None if not found."""
    coll = get_or_create_collection(collection_name)
    result = coll.get(ids=[id], include=["embeddings"])
    if result["ids"]:
        return result["embeddings"][0]
    return None


def get_all_embeddings(collection_name: str):
    """Get all ids and embeddings from a collection."""
    coll = get_or_create_collection(collection_name)
    return coll.get(include=["embeddings", "metadatas"])
