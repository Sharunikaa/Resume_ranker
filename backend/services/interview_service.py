"""
AI interview co-pilot: technical, behavioral, and verification questions.
"""

import asyncio
from typing import Any, Dict, List

from backend.llm import llm_client, prompts


def generate_technical_questions(projects: List[Any]) -> List[str]:
    """Generate project-specific technical questions (can use LLM)."""
    if not projects:
        return []
    summary = "\n".join(
        f"- {p.get('title', '')}: {p.get('description', '')}"
        if isinstance(p, dict)
        else f"- {p.title}: {p.description}"
        for p in projects[:5]
    )
    return _generate_questions_impl(
        experience_summary="N/A",
        projects_summary=summary,
        skill_gaps=[],
        focus="technical",
    )


def generate_behavioral_questions(experience: List[Any], gaps: List[str]) -> List[str]:
    """Generate behavioral questions from experience and gaps."""
    exp_summary = "\n".join(
        f"- {e.get('role', '')} at {e.get('company', '')}: {e.get('description', '')[:150]}"
        if isinstance(e, dict)
        else f"- {e.role} at {e.company}: {e.description[:150]}"
        for e in (experience or [])[:5]
    ) or "N/A"
    return _generate_questions_impl(
        experience_summary=exp_summary,
        projects_summary="N/A",
        skill_gaps=gaps,
        focus="behavioral",
    )


def generate_verification_questions(resume_claims: List[str]) -> List[str]:
    """Generate questions to verify resume claims."""
    claims_str = "\n".join(f"- {c}" for c in (resume_claims or [])[:10]) or "N/A"
    return _generate_questions_impl(
        experience_summary=claims_str,
        projects_summary="N/A",
        skill_gaps=[],
        focus="verification",
    )


def _generate_questions_impl(
    experience_summary: str,
    projects_summary: str,
    skill_gaps: List[str],
    focus: str = "mixed",
) -> List[str]:
    """Call LLM to generate 5 questions."""
    prompt = prompts.INTERVIEW_QUESTIONS_PROMPT.format(
        experience_summary=experience_summary,
        projects_summary=projects_summary,
        skill_gaps=", ".join(skill_gaps) if skill_gaps else "None",
    )
    try:
        response = asyncio.run(llm_client.call_llm(prompt, temperature=0.5))
        data = llm_client.parse_json_response(response)
        questions = data.get("questions", [])
        return questions[:5] if isinstance(questions, list) else []
    except Exception:
        return []


def generate_interview_questions(
    projects: List[Any],
    experience: List[Any],
    skill_gaps: List[str],
) -> List[str]:
    """
    Combined: generate 5 personalized questions (technical + behavioral + verification).
    """
    all_questions = []
    tech = generate_technical_questions(projects)
    behavioral = generate_behavioral_questions(experience, skill_gaps)
    claims = []
    for e in (experience or [])[:3]:
        if isinstance(e, dict):
            claims.append(e.get("description", "")[:100])
        else:
            claims.append(getattr(e, "description", "")[:100])
    verification = generate_verification_questions(claims)
    for q in tech[:2]:
        all_questions.append(q)
    for q in behavioral[:2]:
        all_questions.append(q)
    for q in verification[:1]:
        all_questions.append(q)
    while len(all_questions) < 5 and (tech or behavioral or verification):
        if tech and tech[-1] not in all_questions:
            all_questions.append(tech[-1])
        elif behavioral and behavioral[-1] not in all_questions:
            all_questions.append(behavioral[-1])
        elif verification and verification[-1] not in all_questions:
            all_questions.append(verification[-1])
        else:
            break
    return all_questions[:5]
