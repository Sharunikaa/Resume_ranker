"""
Secure storage for application settings (API keys, etc.)
Uses simple encryption for API keys in MongoDB.
"""

import os
from typing import Optional
from cryptography.fernet import Fernet
from backend.database import mongo


def _get_encryption_key() -> bytes:
    """
    Get or create encryption key for API keys.
    In production, store this in a secure vault (not in code/env).
    """
    key_env = os.getenv("ENCRYPTION_KEY")
    if key_env:
        return key_env.encode()
    
    # Generate a key if not exists (for development)
    # WARNING: In production, use a proper key management system
    key = Fernet.generate_key()
    return key


def _encrypt(value: str) -> str:
    """Encrypt a string value."""
    if not value:
        return ""
    fernet = Fernet(_get_encryption_key())
    return fernet.encrypt(value.encode()).decode()


def _decrypt(encrypted_value: str) -> str:
    """Decrypt an encrypted value."""
    if not encrypted_value:
        return ""
    try:
        fernet = Fernet(_get_encryption_key())
        return fernet.decrypt(encrypted_value.encode()).decode()
    except Exception:
        return ""


def save_api_keys(gemini_key: Optional[str] = None, groq_key: Optional[str] = None) -> None:
    """
    Save API keys to database (encrypted).
    """
    coll = mongo.get_db().settings
    
    update_doc = {}
    if gemini_key is not None:
        update_doc["gemini_api_key_encrypted"] = _encrypt(gemini_key) if gemini_key else ""
    if groq_key is not None:
        update_doc["groq_api_key_encrypted"] = _encrypt(groq_key) if groq_key else ""
    
    if update_doc:
        coll.update_one(
            {"_id": "api_keys"},
            {"$set": update_doc},
            upsert=True
        )


def get_api_keys() -> dict:
    """
    Get API keys from database (decrypted).
    Returns dict with 'gemini_api_key' and 'groq_api_key' (or empty strings).
    """
    coll = mongo.get_db().settings
    doc = coll.find_one({"_id": "api_keys"})
    
    if not doc:
        return {"gemini_api_key": "", "groq_api_key": ""}
    
    return {
        "gemini_api_key": _decrypt(doc.get("gemini_api_key_encrypted", "")),
        "groq_api_key": _decrypt(doc.get("groq_api_key_encrypted", "")),
    }


def clear_api_keys() -> None:
    """Clear all API keys from database."""
    coll = mongo.get_db().settings
    coll.delete_one({"_id": "api_keys"})
