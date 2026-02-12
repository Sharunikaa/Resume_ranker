"""
Candidate detail and compare endpoints.
"""

from typing import List

from fastapi import APIRouter, HTTPException

from backend.database import mongo
from backend.models.candidate_model import CandidateResponse, CareerInsights, CompareCandidatesRequest, Scores, StructuredResume

router = APIRouter()


def _candidate_doc_to_response(doc: dict) -> CandidateResponse:
    resume = doc.get("structured_resume") or {}
    scores = doc.get("scores") or {}
    insights = doc.get("career_insights") or {}
    return CandidateResponse(
        candidate_id=doc["candidate_id"],
        job_id=doc["job_id"],
        name=doc.get("name", ""),
        email=doc.get("email", ""),
        structured_resume=StructuredResume(**resume) if isinstance(resume, dict) else resume,
        scores=Scores(**scores) if isinstance(scores, dict) else scores,
        career_insights=CareerInsights(**insights) if isinstance(insights, dict) else insights,
        rank=doc.get("rank"),
        explanation=doc.get("explanation", ""),
        skill_gaps=doc.get("skill_gaps", []),
        interview_questions=doc.get("interview_questions", []),
        created_at=doc.get("created_at"),
    )


@router.get("/candidates/{candidate_id}", response_model=CandidateResponse)
def get_candidate(candidate_id: str):
    """Get full candidate details."""
    doc = mongo.get_candidates_collection().find_one({"candidate_id": candidate_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return _candidate_doc_to_response(doc)


@router.post("/candidates/compare")
def compare_candidates(payload: CompareCandidatesRequest):
    """Compare 2-5 candidates; return list of candidate details for side-by-side view."""
    if len(payload.candidate_ids) < 2 or len(payload.candidate_ids) > 5:
        raise HTTPException(status_code=400, detail="Provide between 2 and 5 candidate_ids")
    coll = mongo.get_candidates_collection()
    candidates = []
    for cid in payload.candidate_ids:
        doc = coll.find_one({"candidate_id": cid})
        if not doc:
            raise HTTPException(status_code=404, detail=f"Candidate not found: {cid}")
        candidates.append(_candidate_doc_to_response(doc))
    return {"candidates": [c.model_dump() for c in candidates]}
