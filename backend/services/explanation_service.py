"""
AI-generated explanation: summary, strengths, missing skills, recommendation.
"""

import asyncio
from typing import Any, Dict, List

from backend.llm import llm_client, prompts
from backend.models.candidate_model import Scores
from backend.models.job_model import ExtractedRequirements


async def generate_explanation(
    job_requirements: ExtractedRequirements,
    candidate_data: Dict[str, Any],
    scores: Scores | Dict[str, float],
) -> str:
    """
    Generate explanation text (summary + strengths + missing + recommendation).
    Returns a single string suitable for display; can also return structured JSON.
    """
    requirements_str = (
        f"Required skills: {', '.join(job_requirements.required_skills or [])}\n"
        f"Preferred skills: {', '.join(job_requirements.preferred_skills or [])}\n"
        f"Domain: {job_requirements.domain}, Level: {job_requirements.experience_level}"
    )
    projects = candidate_data.get("projects", [])
    projects_str = "\n".join(
        f"- {p.get('title', '')}: {p.get('description', '')[:200]}..."
        if isinstance(p, dict)
        else f"- {p.title}: {p.description[:200]}..."
        for p in (projects or [])[:5]
    ) or "None listed"

    if isinstance(scores, dict):
        project_sim = scores.get("project_similarity", 0) or 0
        skill_m = scores.get("skill_match", 0) or 0
        exp_m = scores.get("experience_match", 0) or 0
        final = scores.get("final_score", 0) or 0
    else:
        project_sim = scores.project_similarity
        skill_m = scores.skill_match
        exp_m = scores.experience_match
        final = scores.final_score
    prompt = prompts.EXPLANATION_PROMPT.format(
        requirements=requirements_str,
        projects=projects_str,
        project_similarity=round(project_sim, 2),
        skill_match=round(skill_m * 100, 1),
        experience_match=round(exp_m * 100, 1),
        final_score=round(final * 100, 1),
    )
    response = await llm_client.call_llm(prompt, temperature=0.3)
    try:
        data = llm_client.parse_json_response(response)
        summary = data.get("summary", "")
        strengths = data.get("top_3_strengths", [])
        missing = data.get("top_3_missing_skills", [])
        rec = data.get("recommendation", "")
        parts = [summary]
        if strengths:
            parts.append("\nTop strengths: " + "; ".join(strengths))
        if missing:
            parts.append("\nMissing skills: " + "; ".join(missing))
        if rec:
            parts.append(f"\nRecommendation: {rec}")
        return "\n".join(parts).strip()
    except Exception:
        return response.strip() if response else ""
