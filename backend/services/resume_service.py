"""
Resume parsing, structured extraction via LLM, and candidate storage.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from backend.database import mongo
from backend.llm import llm_client, prompts
from backend.models.candidate_model import (
    EducationEntry,
    ExperienceEntry,
    ProjectEntry,
    StructuredResume,
)
from backend.services import embedding_service
from backend.vector_store import chroma_client
from utils.parser import extract_text_from_pdf


def parse_resume(file: Union[str, bytes, Any]) -> str:
    """Extract raw text from PDF file."""
    return extract_text_from_pdf(file)


def extract_structured_data(text: str) -> Dict[str, Any]:
    """
    Use LLM to extract structured JSON: name, email, skills, experience, projects, education.
    """
    import asyncio
    prompt = prompts.RESUME_EXTRACTION_PROMPT.format(resume_text=text[:15000])
    response = asyncio.run(llm_client.call_llm(prompt, temperature=0.2))
    data = llm_client.parse_json_response(response)

    def to_exp(e: dict) -> ExperienceEntry:
        return ExperienceEntry(
            company=e.get("company", "") or "",
            role=e.get("role", "") or "",
            duration=e.get("duration", "") or "",
            description=e.get("description", "") or "",
        )

    def to_proj(p: dict) -> ProjectEntry:
        return ProjectEntry(
            title=p.get("title", "") or "",
            description=p.get("description", "") or "",
            technologies=p.get("technologies", []) or [],
            impact=p.get("impact", "") or "",
        )

    def to_edu(ed: dict) -> EducationEntry:
        return EducationEntry(
            degree=ed.get("degree", "") or "",
            institution=ed.get("institution", "") or "",
            year=ed.get("year", "") or "",
        )

    return {
        "name": data.get("name", "") or "",
        "email": data.get("email", "") or "",
        "skills": data.get("skills", []) or [],
        "experience": [to_exp(x) for x in (data.get("experience") or [])],
        "projects": [to_proj(x) for x in (data.get("projects") or [])],
        "education": [to_edu(x) for x in (data.get("education") or [])],
    }


def store_candidate(job_id: str, structured_data: Dict[str, Any]) -> str:
    """
    Store candidate in MongoDB and store embedding in ChromaDB. Returns candidate_id.
    """
    candidate_id = str(uuid.uuid4())
    structured_resume = StructuredResume(
        skills=structured_data.get("skills", []),
        experience=[
            e if isinstance(e, ExperienceEntry) else ExperienceEntry(**e)
            for e in structured_data.get("experience", [])
        ],
        projects=[
            p if isinstance(p, ProjectEntry) else ProjectEntry(**p)
            for p in structured_data.get("projects", [])
        ],
        education=[
            ed if isinstance(ed, EducationEntry) else EducationEntry(**ed)
            for ed in structured_data.get("education", [])
        ],
    )
    # Text for embedding: combine skills, experience, projects
    text_parts = [
        " ".join(structured_resume.skills),
        " ".join(
            f"{e.role} {e.company} {e.description}" for e in structured_resume.experience
        ),
        " ".join(
            f"{p.title} {p.description} " + " ".join(p.technologies)
            for p in structured_resume.projects
        ),
    ]
    text_for_embedding = " ".join(text_parts).strip() or "No content"
    embedding = embedding_service.generate_embedding(text_for_embedding)

    coll_name = chroma_client.get_candidates_collection_name(job_id)
    chroma_client.store_embedding(
        coll_name,
        candidate_id,
        embedding,
        {"candidate_id": candidate_id, "job_id": job_id},
    )

    doc = {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "name": structured_data.get("name", "") or "",
        "email": structured_data.get("email", "") or "",
        "structured_resume": structured_resume.model_dump(),
        "scores": {},
        "career_insights": {},
        "rank": None,
        "explanation": "",
        "skill_gaps": [],
        "interview_questions": [],
        "created_at": datetime.utcnow(),
    }
    mongo.get_candidates_collection().insert_one(doc)
    return candidate_id
