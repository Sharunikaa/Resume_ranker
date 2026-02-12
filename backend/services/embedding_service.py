"""
Embedding generation with sentence-transformers and ChromaDB storage.
"""

from typing import List, Optional

from backend.vector_store import chroma_client
from utils.similarity import cosine_similarity

_embedding_model = None
_MODEL_NAME = "all-MiniLM-L6-v2"


def _get_model():
    """Lazy-load sentence-transformers model."""
    global _embedding_model
    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer
        _embedding_model = SentenceTransformer(_MODEL_NAME)
    return _embedding_model


def generate_embedding(text: str) -> List[float]:
    """Generate embedding for text using sentence-transformers."""
    if not text or not text.strip():
        return _get_model().encode(" ", convert_to_numpy=True).tolist()
    return _get_model().encode(text.strip(), convert_to_numpy=True).tolist()


def store_embedding(
    collection_name: str,
    id: str,
    embedding: List[float],
    metadata: Optional[dict] = None,
) -> None:
    """Store embedding in ChromaDB collection."""
    chroma_client.store_embedding(collection_name, id, embedding, metadata)


def get_embedding(collection_name: str, id: str) -> Optional[List[float]]:
    """Retrieve embedding by id from collection."""
    return chroma_client.get_embedding(collection_name, id)


def compute_similarity(
    job_embedding: List[float],
    candidate_embedding: List[float],
) -> float:
    """Cosine similarity between job and candidate embeddings. Returns 0-1 scale (cosine is -1 to 1, we map to 0-1)."""
    cos = cosine_similarity(job_embedding, candidate_embedding)
    return max(0.0, min(1.0, (cos + 1) / 2))
