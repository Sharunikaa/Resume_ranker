"""
MongoDB connection manager.
Uses singleton client from env (MONGODB_URI, DATABASE_NAME).
"""

import os
from typing import Optional

from pymongo import MongoClient
from pymongo.database import Database

_client: Optional[MongoClient] = None


def get_client() -> MongoClient:
    """Get or create MongoDB client singleton."""
    global _client
    if _client is None:
        uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        _client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    return _client


def get_db() -> Database:
    """Get database by DATABASE_NAME."""
    db_name = os.getenv("DATABASE_NAME", "resume_ranker")
    return get_client()[db_name]


def get_jobs_collection():
    """Get jobs collection."""
    return get_db().jobs


def get_candidates_collection():
    """Get candidates collection."""
    return get_db().candidates


def close_client() -> None:
    """Close MongoDB client (e.g. on shutdown)."""
    global _client
    if _client is not None:
        _client.close()
        _client = None
