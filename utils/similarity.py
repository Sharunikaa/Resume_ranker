"""
Similarity utilities: cosine similarity and skill match percentage.
"""

from typing import List, Sequence


def cosine_similarity(vec1: Sequence[float], vec2: Sequence[float]) -> float:
    """Compute cosine similarity between two vectors."""
    if len(vec1) != len(vec2):
        raise ValueError("Vectors must have same length")
    if len(vec1) == 0:
        return 0.0
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = sum(a * a for a in vec1) ** 0.5
    norm2 = sum(b * b for b in vec2) ** 0.5
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def skill_match_percentage(
    required: List[str],
    candidate: List[str],
    normalize: bool = True,
) -> float:
    """
    Percentage of required skills that appear in candidate skills.
    Optionally normalize skill strings (lowercase, strip).
    """
    if not required:
        return 100.0
    if normalize:
        req_set = {s.lower().strip() for s in required if s and s.strip()}
        cand_set = {s.lower().strip() for s in candidate if s and s.strip()}
    else:
        req_set = set(required)
        cand_set = set(candidate)
    if not req_set:
        return 100.0
    matched = sum(1 for s in req_set if s in cand_set or _fuzzy_match(s, cand_set))
    return 100.0 * matched / len(req_set)


def _fuzzy_match(skill: str, candidate_set: set) -> bool:
    """Check if skill is contained in any candidate skill or vice versa."""
    skill_lower = skill.lower()
    for c in candidate_set:
        c_lower = c.lower()
        if skill_lower in c_lower or c_lower in skill_lower:
            return True
    return False
