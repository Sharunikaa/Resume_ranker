"""
Career trajectory analysis: learning velocity, skill evolution, adaptability.
"""

import asyncio
from typing import Any, Dict, List

from backend.llm import llm_client, prompts


def analyze_career_progression(experience_list: List[Any]) -> Dict[str, Any]:
    """
    Detect growth patterns from experience list (roles, duration).
    Returns dict with progression indicators.
    """
    if not experience_list:
        return {"progression": "unknown", "role_count": 0, "durations": []}
    role_count = len(experience_list)
    durations = []
    for exp in experience_list:
        d = exp.get("duration", "") if isinstance(exp, dict) else getattr(exp, "duration", "")
        durations.append(d or "")
    return {
        "progression": "moderate" if role_count >= 2 else "early",
        "role_count": role_count,
        "durations": durations,
    }


def calculate_learning_velocity(skills_timeline: List[Any]) -> float:
    """
    Rate of skill acquisition (0-10). Simplified: infer from number of roles/projects.
    """
    if not skills_timeline:
        return 5.0
    n = len(skills_timeline)
    if n >= 5:
        return 8.0
    if n >= 3:
        return 6.5
    if n >= 1:
        return 5.0
    return 4.0


def predict_future_potential() -> str:
    """Placeholder: 5-year growth projection. Can be LLM-enhanced."""
    return "Strong growth potential with continued exposure to relevant projects."


def generate_adaptability_score() -> float:
    """Placeholder: 0-100. Can be derived from role diversity and skill breadth."""
    return 70.0


def get_career_insights(
    experience_list: List[Any],
    projects_list: List[Any],
) -> Dict[str, Any]:
    """
    Full career insights: learning_velocity, skill_evolution_rate, adaptability_score.
    Uses LLM when available for narrative.
    """
    progression = analyze_career_progression(experience_list)
    skills_timeline = experience_list + projects_list  # proxy for skill accumulation
    learning_velocity = calculate_learning_velocity(skills_timeline)
    adaptability = generate_adaptability_score()

    exp_str = "\n".join(
        str(e) for e in experience_list[:10]
    )
    proj_str = "\n".join(
        str(p) for p in projects_list[:10]
    )
    prompt = prompts.TRAJECTORY_PROMPT.format(
        experience_list=exp_str or "None",
        projects_list=proj_str or "None",
    )
    try:
        response = asyncio.run(llm_client.call_llm(prompt, temperature=0.3))
        data = llm_client.parse_json_response(response)
        return {
            "learning_velocity": data.get("learning_velocity", learning_velocity),
            "skill_evolution_rate": data.get("skill_evolution_rate", "moderate"),
            "adaptability_score": data.get("adaptability_score", adaptability),
        }
    except Exception:
        return {
            "learning_velocity": learning_velocity,
            "skill_evolution_rate": progression.get("progression", "moderate"),
            "adaptability_score": adaptability,
        }
