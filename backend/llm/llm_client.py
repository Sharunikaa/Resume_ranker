"""
LLM client: Gemini primary, Groq fallback.
Async call_llm, parse_json_response. Load GEMINI_API_KEY / GROQ_API_KEY from env.
"""

import asyncio
import json
import os
import re
from typing import Any, Optional

# Prefer new SDK; fallback for older envs
try:
    from google import genai
    _USE_NEW_SDK = True
except ImportError:
    genai = None
    _USE_NEW_SDK = False

_GEMINI_CLIENT = None
_GROQ_CLIENT = None


def _get_gemini_client():
    """Get or create Gemini client. Returns None if not configured."""
    global _GEMINI_CLIENT
    if _GEMINI_CLIENT is not None:
        return _GEMINI_CLIENT
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        return None
    if _USE_NEW_SDK and genai is not None:
        _GEMINI_CLIENT = genai.Client(api_key=api_key)
        return _GEMINI_CLIENT
    try:
        import google.generativeai as genai_legacy
        genai_legacy.configure(api_key=api_key)
        _GEMINI_CLIENT = genai_legacy
        return _GEMINI_CLIENT
    except Exception:
        return None


def _get_groq_client():
    """Get or create Groq client. Returns None if not configured."""
    global _GROQ_CLIENT
    if _GROQ_CLIENT is not None:
        return _GROQ_CLIENT
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key.strip() == "":
        return None
    try:
        from groq import Groq
        _GROQ_CLIENT = Groq(api_key=api_key.strip())
        return _GROQ_CLIENT
    except Exception:
        return None


def _get_gemini_model() -> str:
    return os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def _get_groq_model() -> str:
    return os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


async def _call_gemini(prompt: str, system_message: Optional[str], temperature: float) -> str:
    """Call Gemini; raises on failure."""
    client = _get_gemini_client()
    if client is None:
        raise ValueError("GEMINI_API_KEY must be set in environment")
    model_name = _get_gemini_model()
    full_content = (system_message or "") + ("\n\n" if system_message else "") + prompt

    if _USE_NEW_SDK and hasattr(client, "aio"):
        response = await client.aio.models.generate_content(
            model=model_name,
            contents=full_content,
            config={"temperature": temperature},
        )
        if response and response.text:
            return response.text.strip()
        return ""

    def _sync():
        model = client.GenerativeModel(model_name)
        resp = model.generate_content(full_content)
        return resp.text.strip() if resp and resp.text else ""
    return await asyncio.to_thread(_sync)


def _call_groq_sync(prompt: str, system_message: Optional[str], temperature: float) -> str:
    """Call Groq (sync). Raises on failure."""
    client = _get_groq_client()
    if client is None:
        raise ValueError("GROQ_API_KEY must be set in environment for fallback")
    model = _get_groq_model()
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    if response.choices and response.choices[0].message.content:
        return response.choices[0].message.content.strip()
    return ""


async def call_llm(
    prompt: str,
    system_message: Optional[str] = None,
    temperature: float = 0.2,
    use_cache: bool = True,
    max_retries: int = 3,
) -> str:
    """
    Call LLM with caching and automatic retry: try Gemini first, then Groq on failure.
    Retries with exponential backoff on transient errors.
    Returns the model text response.
    """
    import time
    
    # Build full prompt for caching
    full_prompt = (system_message or "") + ("\n\n" if system_message else "") + prompt
    
    # Try cache first
    if use_cache:
        from backend.database import cache
        # Try to get from cache (check both Gemini and Groq model names)
        gemini_model = _get_gemini_model()
        groq_model = _get_groq_model()
        
        cached = cache.get_cached_response(full_prompt, gemini_model, temperature)
        if cached:
            return cached
        cached = cache.get_cached_response(full_prompt, groq_model, temperature)
        if cached:
            return cached
    
    # Retry loop with exponential backoff
    last_error = None
    for attempt in range(max_retries):
        try:
            response = None
            model_used = None
            
            # Try Gemini first if configured
            if _get_gemini_client() is not None:
                try:
                    response = await _call_gemini(prompt, system_message, temperature)
                    model_used = _get_gemini_model()
                except Exception as e:
                    err_msg = str(e).lower()
                    # Fall back to Groq on quota/rate-limit or other transient errors
                    if "429" in err_msg or "quota" in err_msg or "resource_exhausted" in err_msg or "rate" in err_msg:
                        if _get_groq_client() is not None:
                            response = await asyncio.to_thread(
                                _call_groq_sync, prompt, system_message, temperature
                            )
                            model_used = _get_groq_model()
                        else:
                            raise
                    else:
                        raise

            # No Gemini: use Groq if configured
            if response is None and _get_groq_client() is not None:
                response = await asyncio.to_thread(
                    _call_groq_sync, prompt, system_message, temperature
                )
                model_used = _get_groq_model()

            if response is None:
                raise ValueError(
                    "Set at least one of GEMINI_API_KEY or GROQ_API_KEY in environment"
                )
            
            # Cache the response
            if use_cache and model_used:
                from backend.database import cache
                cache.cache_response(full_prompt, model_used, temperature, response)
            
            return response
            
        except Exception as e:
            last_error = e
            err_msg = str(e).lower()
            
            # Check if error is retryable
            is_retryable = any(keyword in err_msg for keyword in [
                "429", "quota", "resource_exhausted", "rate", "timeout",
                "connection", "network", "unavailable", "overloaded"
            ])
            
            if is_retryable and attempt < max_retries - 1:
                # Exponential backoff: 2^attempt seconds (2s, 4s, 8s)
                wait_time = 2 ** attempt
                print(f"LLM call failed (attempt {attempt + 1}/{max_retries}): {e}")
                print(f"Retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)
            else:
                # Non-retryable error or max retries reached
                break
    
    # All retries failed
    raise Exception(f"LLM call failed after {max_retries} attempts: {last_error}")


def parse_json_response(response: str) -> Any:
    """
    Parse JSON from LLM response. Handles markdown code blocks.
    """
    text = response.strip()
    # Strip markdown code block if present
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        text = match.group(1).strip()
    return json.loads(text)
