"""
Settings API routes: save/retrieve API keys.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from backend.database import settings

router = APIRouter()


class APIKeysRequest(BaseModel):
    gemini_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None


class APIKeysResponse(BaseModel):
    gemini_api_key: str
    groq_api_key: str


@router.post("/settings/api-keys")
def save_api_keys(payload: APIKeysRequest):
    """Save API keys (encrypted in database)."""
    try:
        settings.save_api_keys(
            gemini_key=payload.gemini_api_key,
            groq_key=payload.groq_api_key
        )
        return {"message": "API keys saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/settings/api-keys", response_model=APIKeysResponse)
def get_api_keys():
    """Get API keys (decrypted from database)."""
    try:
        keys = settings.get_api_keys()
        # Mask the keys for security (show only first 10 chars)
        return {
            "gemini_api_key": keys["gemini_api_key"][:10] + "..." if keys["gemini_api_key"] else "",
            "groq_api_key": keys["groq_api_key"][:10] + "..." if keys["groq_api_key"] else "",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/settings/api-keys")
def clear_api_keys():
    """Clear all API keys."""
    try:
        settings.clear_api_keys()
        return {"message": "API keys cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
