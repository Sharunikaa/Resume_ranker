"""
Job creation and requirement extraction using LLM.
"""

import uuid
from datetime import datetime
from typing import List, Optional

from backend.database import mongo
from backend.llm import llm_client, prompts
from backend.models.job_model import ExtractedRequirements, JobCreate, JobResponse, Weights
from backend.services import embedding_service
from backend.vector_store import chroma_client


def create_job(title: str, description: str) -> JobResponse:
    """
    Create a job: extract requirements via LLM, store in MongoDB, generate job embedding.
    """
    job_id = str(uuid.uuid4())
    requirements = _extract_requirements(description)
    weights = Weights(project_weight=0.4, skill_weight=0.35, experience_weight=0.25)
    doc = {
        "job_id": job_id,
        "title": title,
        "description": description,
        "extracted_requirements": requirements.model_dump(),
        "weights": weights.model_dump(),
        "created_at": datetime.utcnow(),
    }
    coll = mongo.get_jobs_collection()
    coll.insert_one(doc)

    # Generate and store job embedding for project/semantic similarity
    emb = embedding_service.generate_embedding(description)
    coll_name = chroma_client.get_job_embeddings_collection_name(job_id)
    chroma_client.store_embedding(coll_name, job_id, emb, {"job_id": job_id})

    return JobResponse(
        job_id=doc["job_id"],
        title=doc["title"],
        description=doc["description"],
        extracted_requirements=ExtractedRequirements(**doc["extracted_requirements"]),
        weights=weights,
        created_at=doc["created_at"],
    )


def _extract_requirements(description: str) -> ExtractedRequirements:
    """Use LLM to extract required_skills, preferred_skills, domain, experience_level."""
    import asyncio
    prompt = prompts.JOB_EXTRACTION_PROMPT.format(job_description=description)
    response = asyncio.run(llm_client.call_llm(prompt, temperature=0.2))
    data = llm_client.parse_json_response(response)
    return ExtractedRequirements(
        required_skills=data.get("required_skills", []) or [],
        preferred_skills=data.get("preferred_skills", []) or [],
        domain=data.get("domain", "") or "",
        experience_level=(data.get("experience_level") or "").lower().strip() or "",
    )


def get_job(job_id: str) -> Optional[JobResponse]:
    """Get job by id."""
    coll = mongo.get_jobs_collection()
    doc = coll.find_one({"job_id": job_id})
    if not doc:
        return None
    return _doc_to_job_response(doc)


def list_jobs() -> List[JobResponse]:
    """List all jobs, newest first."""
    coll = mongo.get_jobs_collection()
    cursor = coll.find().sort("created_at", -1)
    return [_doc_to_job_response(doc) for doc in cursor]


def update_job(job_id: str, description: str) -> Optional[JobResponse]:
    """
    Update job description: re-extract requirements, update MongoDB, regenerate embedding.
    """
    coll = mongo.get_jobs_collection()
    doc = coll.find_one({"job_id": job_id})
    if not doc:
        return None
    
    # Re-extract requirements from new description
    requirements = _extract_requirements(description)
    
    # Update MongoDB
    coll.update_one(
        {"job_id": job_id},
        {
            "$set": {
                "description": description,
                "extracted_requirements": requirements.model_dump(),
                "updated_at": datetime.utcnow(),
            }
        },
    )
    
    # Regenerate and update job embedding
    emb = embedding_service.generate_embedding(description)
    coll_name = chroma_client.get_job_embeddings_collection_name(job_id)
    chroma_client.store_embedding(coll_name, job_id, emb, {"job_id": job_id})
    
    # Return updated job
    return get_job(job_id)


def generate_job_embedding(description: str):
    """Generate embedding for job description (used when storing job)."""
    return embedding_service.generate_embedding(description)


def _doc_to_job_response(doc: dict) -> JobResponse:
    return JobResponse(
        job_id=doc["job_id"],
        title=doc["title"],
        description=doc["description"],
        extracted_requirements=ExtractedRequirements(**doc.get("extracted_requirements", {})),
        weights=Weights(**doc.get("weights", {})),
        created_at=doc.get("created_at"),
    )
