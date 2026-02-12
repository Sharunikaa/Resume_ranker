"""
Scoring and ranking: skill match, experience match, final score, rank assignment.
"""

from typing import Any, Dict, List, Optional

from backend.database import mongo
from backend.models.job_model import ExtractedRequirements, Weights
from backend.services import embedding_service
from backend.vector_store import chroma_client
from utils.similarity import skill_match_percentage


def calculate_skill_match(
    job_skills: List[str],
    candidate_skills: List[str],
) -> float:
    """Percentage match (0-100) of required skills in candidate skills. Normalized to 0-1 for scoring."""
    pct = skill_match_percentage(job_skills, candidate_skills)
    return pct / 100.0


def calculate_experience_match(
    job_requirements: ExtractedRequirements,
    candidate_experience: List[Any],
) -> float:
    """
    Heuristic experience match: level alignment and relevance.
    Returns 0-1 score.
    """
    level = (job_requirements.experience_level or "").lower()
    if not level or not candidate_experience:
        return 0.5  # neutral if no data

    years = 0.0
    for exp in candidate_experience:
        d = getattr(exp, "duration", None) or (exp.get("duration") if isinstance(exp, dict) else "")
        if isinstance(exp, dict):
            desc = exp.get("description", "") or exp.get("role", "")
        else:
            desc = getattr(exp, "description", "") or getattr(exp, "role", "")
        # Rough duration parsing (e.g. "2 years", "2020-2022")
        s = (d or "") + " " + (desc or "")
        if "year" in s.lower():
            years += 1.0
        if any(x in (d or "").lower() for x in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]):
            years += 0.5

    if level == "junior":
        return min(1.0, 0.3 + years * 0.2)
    if level == "mid":
        return min(1.0, 0.2 + years * 0.25)
    if level == "senior" or level == "lead":
        return min(1.0, 0.1 + years * 0.2)
    return 0.5


def calculate_final_score(
    project_sim: float,
    skill_match: float,
    exp_match: float,
    weights: Weights,
) -> float:
    """Weighted final score in 0-1 range."""
    return (
        weights.project_weight * project_sim
        + weights.skill_weight * skill_match
        + weights.experience_weight * exp_match
    )


def rank_all_candidates(job_id: str) -> List[str]:
    """
    Compute scores for all candidates of a job, sort by final_score, assign ranks.
    Updates MongoDB. Returns list of candidate_ids in rank order.
    """
    job_coll = mongo.get_jobs_collection()
    cand_coll = mongo.get_candidates_collection()
    job_doc = job_coll.find_one({"job_id": job_id})
    if not job_doc:
        return []

    weights = Weights(**job_doc.get("weights", {}))
    req = ExtractedRequirements(**job_doc.get("extracted_requirements", {}))

    # Job embedding for project similarity
    coll_name = chroma_client.get_candidates_collection_name(job_id)
    job_emb_coll_name = chroma_client.get_job_embeddings_collection_name(job_id)
    job_emb = chroma_client.get_embedding(job_emb_coll_name, job_id)
    if job_emb is None or len(job_emb) == 0:
        job_emb = embedding_service.generate_embedding(job_doc.get("description", ""))
        chroma_client.store_embedding(job_emb_coll_name, job_id, job_emb, {"job_id": job_id})

    all_data = chroma_client.get_all_embeddings(coll_name)
    ids = all_data.get("ids") if all_data.get("ids") is not None else []
    embeddings = all_data.get("embeddings") if all_data.get("embeddings") is not None else []

    candidates = list(cand_coll.find({"job_id": job_id}))
    results = []
    for c in candidates:
        cid = c["candidate_id"]
        cand_emb = None
        if cid in ids:
            idx = ids.index(cid)
            cand_emb = embeddings[idx] if idx < len(embeddings) else None
        if cand_emb is None or (isinstance(cand_emb, list) and len(cand_emb) == 0):
            continue
        project_sim = embedding_service.compute_similarity(job_emb, cand_emb)

        resume = c.get("structured_resume") or {}
        if isinstance(resume, dict):
            skills = resume.get("skills", [])
            experience = resume.get("experience", [])
        else:
            skills = getattr(resume, "skills", [])
            experience = getattr(resume, "experience", [])

        skill_match = calculate_skill_match(req.required_skills, skills)
        exp_match = calculate_experience_match(req, experience)
        final = calculate_final_score(project_sim, skill_match, exp_match, weights)

        results.append({
            "candidate_id": cid,
            "project_similarity": project_sim,
            "skill_match": skill_match,
            "experience_match": exp_match,
            "final_score": final,
        })

    results.sort(key=lambda x: x["final_score"], reverse=True)
    for rank, r in enumerate(results, start=1):
        cand_coll.update_one(
            {"candidate_id": r["candidate_id"]},
            {
                "$set": {
                    "scores": {
                        "project_similarity": r["project_similarity"],
                        "skill_match": r["skill_match"],
                        "experience_match": r["experience_match"],
                        "final_score": r["final_score"],
                    },
                    "rank": rank,
                },
            },
        )
    return [r["candidate_id"] for r in results]
