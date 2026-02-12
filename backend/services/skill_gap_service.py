"""
Skill gap identification, learning path suggestions, training time estimates.
"""

from typing import List, Tuple


def identify_skill_gaps(
    required_skills: List[str],
    candidate_skills: List[str],
) -> List[str]:
    """
    Return list of required skills that the candidate does not have.
    Uses normalized comparison and simple substring matching.
    """
    req_set = {s.lower().strip() for s in required_skills if s and s.strip()}
    cand_set = {s.lower().strip() for s in candidate_skills if s and s.strip()}
    missing = []
    for r in req_set:
        if r in cand_set:
            continue
        if any(r in c or c in r for c in cand_set):
            continue
        missing.append(r)
    return missing


def suggest_learning_path(missing_skills: List[str]) -> List[Tuple[str, str]]:
    """
    For each missing skill, suggest a learning resource (placeholder).
    Returns list of (skill, suggestion).
    """
    suggestions = []
    for s in missing_skills:
        suggestions.append((s, f"Consider online courses or certifications for {s}."))
    return suggestions


def estimate_training_time(skill: str) -> str:
    """Rough estimate (placeholder)."""
    skill_lower = skill.lower()
    if any(x in skill_lower for x in ["python", "javascript", "sql"]):
        return "2-4 weeks"
    if any(x in skill_lower for x in ["machine learning", "aws", "cloud"]):
        return "1-3 months"
    return "1-2 months"
