"""
Ranking trigger and get rankings.
"""

import asyncio
from typing import List

from fastapi import APIRouter, HTTPException

from backend.database import mongo
from backend.models.candidate_model import CandidateResponse, CareerInsights, Scores, StructuredResume
from backend.models.job_model import ExtractedRequirements
from backend.services import explanation_service, interview_service, ranking_service, skill_gap_service, trajectory_service

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


@router.post("/jobs/{job_id}/rank")
async def trigger_ranking(job_id: str):
    """Compute scores, rank candidates, then generate explanation, trajectory, skill_gaps, interview_questions for each."""
    import time
    
    job_doc = mongo.get_jobs_collection().find_one({"job_id": job_id})
    if not job_doc:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Retry ranking with exponential backoff
    max_retries = 3
    candidate_ids = None
    last_error = None
    
    for attempt in range(max_retries):
        try:
            print(f"\n{'='*60}")
            print(f"Ranking attempt {attempt + 1}/{max_retries} for job {job_id}")
            print(f"{'='*60}\n")
            candidate_ids = ranking_service.rank_all_candidates(job_id)
            print(f"✓ Ranking successful: {len(candidate_ids)} candidates scored")
            break
        except Exception as e:
            last_error = e
            print(f"✗ Ranking failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"✗ All ranking attempts failed")
                raise HTTPException(status_code=500, detail=f"Ranking failed after {max_retries} attempts: {str(last_error)}")
    
    if not candidate_ids:
        raise HTTPException(status_code=500, detail="No candidates to rank")

    req = ExtractedRequirements(**job_doc.get("extracted_requirements", {}))
    cand_coll = mongo.get_candidates_collection()
    
    print(f"\n{'='*60}")
    print(f"Generating enrichments for {len(candidate_ids)} candidates")
    print(f"{'='*60}\n")
    
    for idx, cid in enumerate(candidate_ids, 1):
        print(f"[{idx}/{len(candidate_ids)}] Processing candidate {cid}")
        doc = cand_coll.find_one({"candidate_id": cid})
        if not doc:
            print(f"  ✗ Candidate not found in DB")
            continue
        
        resume = doc.get("structured_resume") or {}
        scores_dict = doc.get("scores") or {}
        skills = resume.get("skills", []) if isinstance(resume, dict) else getattr(resume, "skills", [])
        experience = resume.get("experience", []) if isinstance(resume, dict) else getattr(resume, "experience", [])
        projects = resume.get("projects", []) if isinstance(resume, dict) else getattr(resume, "projects", [])

        # Generate enrichments with retry logic
        skill_gaps = []
        explanation = ""
        career_insights = {}
        interview_questions = []
        
        # Skill gaps (with retry)
        for attempt in range(max_retries):
            try:
                skill_gaps = skill_gap_service.identify_skill_gaps(req.required_skills, skills)
                print(f"  ✓ Skill gaps identified")
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"  ⚠ Skill gaps failed (attempt {attempt + 1}), retrying...")
                    await asyncio.sleep(1)
                else:
                    print(f"  ✗ Skill gaps failed after {max_retries} attempts: {e}")
        
        # Explanation (with retry)
        for attempt in range(max_retries):
            try:
                explanation = await explanation_service.generate_explanation(req, resume, scores_dict)
                print(f"  ✓ Explanation generated")
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"  ⚠ Explanation failed (attempt {attempt + 1}), retrying...")
                    await asyncio.sleep(1)
                else:
                    print(f"  ✗ Explanation failed after {max_retries} attempts: {e}")
                    explanation = f"Error generating explanation after {max_retries} attempts"
        
        # Career insights (with retry)
        for attempt in range(max_retries):
            try:
                career_insights = trajectory_service.get_career_insights(experience, projects)
                print(f"  ✓ Career insights generated")
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"  ⚠ Career insights failed (attempt {attempt + 1}), retrying...")
                    await asyncio.sleep(1)
                else:
                    print(f"  ✗ Career insights failed after {max_retries} attempts: {e}")
        
        # Interview questions (with retry)
        for attempt in range(max_retries):
            try:
                interview_questions = interview_service.generate_interview_questions(projects, experience, skill_gaps)
                print(f"  ✓ Interview questions generated")
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"  ⚠ Interview questions failed (attempt {attempt + 1}), retrying...")
                    await asyncio.sleep(1)
                else:
                    print(f"  ✗ Interview questions failed after {max_retries} attempts: {e}")

        cand_coll.update_one(
            {"candidate_id": cid},
            {
                "$set": {
                    "explanation": explanation,
                    "skill_gaps": skill_gaps,
                    "career_insights": career_insights,
                    "interview_questions": interview_questions,
                },
            },
        )
        print(f"  ✓ Candidate enrichments saved to DB\n")
    
    print(f"{'='*60}")
    print(f"✓ All enrichments completed for {len(candidate_ids)} candidates")
    print(f"{'='*60}\n")
    
    return {"ranked_count": len(candidate_ids), "candidate_ids": candidate_ids}


@router.get("/jobs/{job_id}/rankings", response_model=List[CandidateResponse])
def get_rankings(job_id: str):
    """Get ranked candidates for a job."""
    job = mongo.get_jobs_collection().find_one({"job_id": job_id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    docs = list(mongo.get_candidates_collection().find({"job_id": job_id}).sort("rank", 1))
    return [_candidate_doc_to_response(d) for d in docs]


@router.post("/candidates/{candidate_id}/rescore")
async def rescore_candidate(candidate_id: str):
    """Rescore a single candidate (force refresh of scores and explanations)."""
    try:
        # Get candidate's job_id
        cand_coll = mongo.get_candidates_collection()
        candidate = cand_coll.find_one({"candidate_id": candidate_id})
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        job_id = candidate.get("job_id")
        if not job_id:
            raise HTTPException(status_code=400, detail="Candidate has no associated job")
        
        # Re-run ranking for this job (will update all candidates including this one)
        # This ensures relative rankings are maintained
        candidate_ids = ranking_service.rank_all_candidates(job_id)
        
        # Get job requirements for enrichments
        job_doc = mongo.get_jobs_collection().find_one({"job_id": job_id})
        if not job_doc:
            raise HTTPException(status_code=404, detail="Job not found")
        
        req = ExtractedRequirements(**job_doc.get("extracted_requirements", {}))
        
        # Re-generate enrichments for all candidates
        for cid in candidate_ids:
            doc = cand_coll.find_one({"candidate_id": cid})
            if not doc:
                continue
            resume = doc.get("structured_resume") or {}
            scores_dict = doc.get("scores") or {}
            skills = resume.get("skills", []) if isinstance(resume, dict) else getattr(resume, "skills", [])
            experience = resume.get("experience", []) if isinstance(resume, dict) else getattr(resume, "experience", [])
            projects = resume.get("projects", []) if isinstance(resume, dict) else getattr(resume, "projects", [])

            # Generate enrichments
            skill_gaps = []
            explanation = ""
            career_insights = {}
            interview_questions = []
            
            try:
                skill_gaps = skill_gap_service.identify_skill_gaps(req.required_skills, skills)
            except Exception as e:
                print(f"Skill gaps failed for {cid}: {e}")
            
            try:
                explanation = await explanation_service.generate_explanation(req, resume, scores_dict)
            except Exception as e:
                print(f"Explanation failed for {cid}: {e}")
                explanation = f"Error generating explanation: {str(e)}"
            
            try:
                career_insights = trajectory_service.get_career_insights(experience, projects)
            except Exception as e:
                print(f"Career insights failed for {cid}: {e}")
            
            try:
                interview_questions = interview_service.generate_interview_questions(projects, experience, skill_gaps)
            except Exception as e:
                print(f"Interview questions failed for {cid}: {e}")

            cand_coll.update_one(
                {"candidate_id": cid},
                {
                    "$set": {
                        "explanation": explanation,
                        "skill_gaps": skill_gaps,
                        "career_insights": career_insights,
                        "interview_questions": interview_questions,
                    },
                },
            )
        
        return {"message": "Candidate rescored successfully", "ranked_count": len(candidate_ids)}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Rescore error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
