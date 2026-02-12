"""
LLM response caching in MongoDB to avoid redundant API calls.
Cache key = hash(prompt + model + temperature).
"""

import hashlib
import json
from datetime import datetime, timedelta
from typing import Optional

from backend.database import mongo


def _get_cache_collection():
    """Get the LLM cache collection."""
    return mongo.get_db().llm_cache


def _generate_cache_key(prompt: str, model: str, temperature: float) -> str:
    """Generate cache key from prompt, model, and temperature."""
    content = f"{prompt}|{model}|{temperature}"
    return hashlib.sha256(content.encode()).hexdigest()


def get_cached_response(prompt: str, model: str, temperature: float, max_age_hours: int = 24) -> Optional[str]:
    """
    Get cached LLM response if exists and not expired.
    Returns None if cache miss or expired.
    """
    cache_key = _generate_cache_key(prompt, model, temperature)
    coll = _get_cache_collection()
    
    doc = coll.find_one({"cache_key": cache_key})
    if not doc:
        return None
    
    # Check expiration
    created_at = doc.get("created_at")
    if created_at:
        age = datetime.utcnow() - created_at
        if age > timedelta(hours=max_age_hours):
            # Expired - delete and return None
            coll.delete_one({"cache_key": cache_key})
            return None
    
    return doc.get("response")


def cache_response(prompt: str, model: str, temperature: float, response: str) -> None:
    """
    Cache LLM response in MongoDB.
    Uses upsert to handle duplicates.
    """
    cache_key = _generate_cache_key(prompt, model, temperature)
    coll = _get_cache_collection()
    
    coll.update_one(
        {"cache_key": cache_key},
        {
            "$set": {
                "cache_key": cache_key,
                "prompt": prompt[:500],  # Store truncated prompt for debugging
                "model": model,
                "temperature": temperature,
                "response": response,
                "created_at": datetime.utcnow(),
            }
        },
        upsert=True,
    )


def clear_expired_cache(max_age_hours: int = 24) -> int:
    """
    Clear expired cache entries.
    Returns count of deleted entries.
    """
    coll = _get_cache_collection()
    cutoff = datetime.utcnow() - timedelta(hours=max_age_hours)
    result = coll.delete_many({"created_at": {"$lt": cutoff}})
    return result.deleted_count


def clear_all_cache() -> int:
    """Clear all cache entries. Returns count deleted."""
    coll = _get_cache_collection()
    result = coll.delete_many({})
    return result.deleted_count
